# ========================================
# Pro-Max AFIS - ML Tasks
# ========================================
# Background tasks for machine learning operations
# Author: Pro-Max Development Team

from app.tasks.celery_app import celery_app
from app.ml.models.forecasting import SalesForecaster
from app.ml.models.health_score import FinancialHealthScorer
from app.models.user import User, Business
from app.models.financial import Transaction
from app.models.ml_predictions import MLPrediction, ModelType, PredictionType, AnomalyDetection, AnomalyType
from app.core.database import SessionLocal
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.tasks.ml_tasks.generate_sales_forecast")
def generate_sales_forecast(
    self,
    business_id: int,
    horizon_days: int = 30,
    model_type: str = "ensemble"
):
    """
    Generate sales forecast for a business
    
    Args:
        business_id: Business ID
        horizon_days: Forecast horizon in days
        model_type: Model type to use
    """
    db = SessionLocal()
    try:
        logger.info(f"Generating sales forecast for business {business_id}")
        
        # Get historical sales data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=365)
        
        transactions = db.query(Transaction).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_type == "income",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).order_by(Transaction.transaction_date).all()
        
        if len(transactions) < 30:
            logger.warning(f"Insufficient data for forecasting business {business_id}")
            return {"status": "failed", "error": "Insufficient data"}
        
        # Prepare data
        dates = [t.transaction_date for t in transactions]
        amounts = [float(t.amount) for t in transactions]
        
        # Generate forecast
        forecaster = SalesForecaster()
        forecast = forecaster.forecast(
            dates=dates,
            amounts=amounts,
            horizon=horizon_days,
            model_type=model_type,
            include_confidence=True,
            include_seasonality=True
        )
        
        # Save prediction to database
        ml_prediction = MLPrediction(
            business_id=business_id,
            prediction_type=PredictionType.SALES_FORECAST,
            model_type=ModelType(model_type),
            prediction_results=forecast,
            confidence_score=forecast.get("confidence_score"),
            prediction_horizon_days=horizon_days,
            seasonal_factors=forecast.get("seasonal_factors"),
            recommendations=forecast.get("inventory_suggestions"),
            prediction_date=end_date
        )
        
        db.add(ml_prediction)
        db.commit()
        
        logger.info(f"Sales forecast generated for business {business_id}")
        
        return {"status": "success", "forecast_id": ml_prediction.id}
        
    except Exception as e:
        logger.error(f"Sales forecast generation failed: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name="app.tasks.ml_tasks.generate_health_score")
def generate_health_score(self, business_id: int):
    """
    Generate financial health score for a business
    
    Args:
        business_id: Business ID
    """
    db = SessionLocal()
    try:
        logger.info(f"Generating health score for business {business_id}")
        
        # Get financial data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=90)  # Last 3 months
        
        transactions = db.query(Transaction).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).all()
        
        # Get business
        business = db.query(Business).filter(Business.id == business_id).first()
        
        # Calculate health score
        scorer = FinancialHealthScorer()
        health_score = scorer.calculate_score(
            financial_data={
                "transactions": transactions,
                "business": business
            },
            business_id=business_id,
            db=db
        )
        
        logger.info(f"Health score generated for business {business_id}: {health_score['overall_score']}")
        
        return {"status": "success", "health_score": health_score}
        
    except Exception as e:
        logger.error(f"Health score generation failed: {str(e)}")
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name="app.tasks.ml_tasks.detect_anomalies")
def detect_anomalies(self, business_id: int):
    """
    Detect anomalies in financial data
    
    Args:
        business_id: Business ID
    """
    db = SessionLocal()
    try:
        logger.info(f"Detecting anomalies for business {business_id}")
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)  # Last 30 days
        
        # Get transactions
        transactions = db.query(Transaction).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).all()
        
        anomalies_detected = []
        
        # Analyze transactions for anomalies
        for transaction in transactions:
            # Check for unusually large amounts
            if transaction.amount > 100000:  # Threshold for large transactions
                anomaly = AnomalyDetection(
                    business_id=business_id,
                    anomaly_type=AnomalyType.UNUSUAL_EXPENSE if transaction.transaction_type == "expense" else AnomalyType.UNUSUAL_INCOME,
                    severity="high",
                    reference_type="transaction",
                    reference_id=transaction.id,
                    anomaly_value=transaction.amount,
                    title=f"Unusual {'Expense' if transaction.transaction_type == 'expense' else 'Income'} Detected",
                    description=f"Transaction of ₹{transaction.amount:,} is unusually large",
                    start_date=transaction.transaction_date,
                    end_date=transaction.transaction_date
                )
                db.add(anomaly)
                anomalies_detected.append(anomaly)
        
        db.commit()
        
        logger.info(f"Detected {len(anomalies_detected)} anomalies for business {business_id}")
        
        return {"status": "success", "anomalies_count": len(anomalies_detected)}
        
    except Exception as e:
        logger.error(f"Anomaly detection failed: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name="app.tasks.ml_tasks.retrain_models")
def retrain_models(self):
    """
    Retrain ML models with latest data
    This is a periodic task scheduled by Celery Beat
    """
    db = SessionLocal()
    try:
        logger.info("Starting ML model retraining")
        
        # Get all businesses with sufficient data
        businesses = db.query(Business).filter(
            Business.is_active == True
        ).all()
        
        retrained_count = 0
        
        for business in businesses:
            try:
                # Check if business has enough data
                transaction_count = db.query(Transaction).filter(
                    Transaction.business_id == business.id
                ).count()
                
                if transaction_count >= 100:
                    # Retrain forecast model
                    generate_sales_forecast.delay(business.id)
                    retrained_count += 1
                    
            except Exception as e:
                logger.error(f"Failed to retrain model for business {business.id}: {str(e)}")
        
        logger.info(f"ML model retraining completed. Retrained {retrained_count} models")
        
        return {"status": "success", "retrained_count": retrained_count}
        
    except Exception as e:
        logger.error(f"ML model retraining failed: {str(e)}")
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name="app.tasks.ml_tasks.process_voice_input")
def process_voice_input(self, audio_data: bytes, language: str, business_id: int, user_id: int):
    """
    Process voice input and generate insights
    
    Args:
        audio_data: Audio data as bytes
        language: Language code
        business_id: Business ID
        user_id: User ID
    """
    try:
        from app.services.voice_service import VoiceService
        from app.ml.agents.financial_agent import FinancialAgent
        
        logger.info(f"Processing voice input for user {user_id}")
        
        # Transcribe audio
        voice_service = VoiceService()
        transcription_result = voice_service.transcribe_audio(audio_data, language)
        
        if not transcription_result["success"]:
            return {"status": "failed", "error": transcription_result.get("error")}
        
        # Process with AI agent
        agent = FinancialAgent()
        agent_result = agent.process_message(
            message=transcription_result["text"],
            language=language,
            business_id=str(business_id),
            user_id=str(user_id),
            db=SessionLocal()
        )
        
        logger.info(f"Voice input processed for user {user_id}")
        
        return {
            "status": "success",
            "transcription": transcription_result,
            "insight": agent_result
        }
        
    except Exception as e:
        logger.error(f"Voice input processing failed: {str(e)}")
        raise