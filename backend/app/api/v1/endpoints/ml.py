# ========================================
# Pro-Max AFIS - Machine Learning Endpoints
# ========================================
# AI-powered financial intelligence and forecasting
# Author: Pro-Max Development Team

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
import logging
import base64

from app.core.config import settings
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.financial import Transaction
from app.ml.models.forecasting import SalesForecaster
from app.ml.models.health_score import FinancialHealthScorer
from app.ml.models.categorization import TransactionCategorizer
from app.ml.agents.financial_agent import FinancialAgent
from app.services.voice_service import VoiceService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize ML models and services
sales_forecaster = SalesForecaster()
health_scorer = FinancialHealthScorer()
transaction_categorizer = TransactionCategorizer()
financial_agent = FinancialAgent()
voice_service = VoiceService()


# ========================================
# Sales Forecasting Endpoints
# ========================================

@router.post("/forecast/sales")
async def forecast_sales(
    horizon_days: int = 30,
    include_confidence_interval: bool = True,
    include_seasonality: bool = True,
    model_type: str = "ensemble",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate sales forecast using ensemble ML models
    
    Uses XGBoost, LightGBM, and Prophet models to predict future sales.
    Provides confidence intervals and inventory suggestions.
    
    - **horizon_days**: Number of days to forecast (default: 30)
    - **include_confidence_interval**: Include confidence bounds in forecast
    - **include_seasonality**: Include seasonal factors in forecast
    - **model_type**: Model to use (xgboost, lightgbm, prophet, ensemble)
    """
    
    try:
        if not settings.enable_ml_predictions:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="ML predictions feature is disabled"
            )
        
        business_id = current_user.business.id
        
        # Get historical sales data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=365)  # Last year of data
        
        transactions = db.query(Transaction).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_type == "income",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).order_by(Transaction.transaction_date).all()
        
        if len(transactions) < 30:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient historical data for forecasting. Need at least 30 days of data."
            )
        
        # Prepare data for forecasting
        dates = [t.transaction_date for t in transactions]
        amounts = [float(t.amount) for t in transactions]
        
        # Generate forecast
        forecast_result = sales_forecaster.forecast(
            dates=dates,
            amounts=amounts,
            horizon=horizon_days,
            model_type=model_type,
            include_confidence=include_confidence_interval,
            include_seasonality=include_seasonality
        )
        
        # Get inventory suggestions based on forecast
        inventory_suggestions = sales_forecaster.get_inventory_suggestions(
            business_id=business_id,
            db=db,
            forecast=forecast_result
        )
        
        logger.info(f"Sales forecast generated for business {business_id}")
        
        return {
            "forecasting_result": {
                "period": f"next_{horizon_days}_days",
                "model_used": model_type,
                "model_version": settings.ml_model_version,
                "predicted_revenue": forecast_result["total_revenue"],
                "confidence_interval": forecast_result.get("confidence_interval"),
                "breakdown": forecast_result["daily_breakdown"],
                "inventory_suggestions": inventory_suggestions,
                "seasonal_factors": forecast_result.get("seasonal_factors", []),
                "generated_at": datetime.utcnow()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Sales forecast failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate sales forecast"
        )


@router.get("/financial-health")
async def get_financial_health_score(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current financial health score (Business Pulse)
    
    Calculates a comprehensive financial health score (0-100) based on:
    - Cash position
    - Profitability
    - Solvency
    - Efficiency
    - Growth
    
    Also provides recommendations for improvement.
    """
    
    try:
        business_id = current_user.business.id
        
        # Get financial data for the last 90 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=90)
        
        transactions = db.query(Transaction).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).all()
        
        # Separate income and expenses
        income_transactions = [t for t in transactions if t.transaction_type == "income"]
        expense_transactions = [t for t in transactions if t.transaction_type == "expense"]
        
        # Calculate financial metrics
        financial_data = {
            "total_income": sum(t.amount for t in income_transactions),
            "total_expenses": sum(t.amount for t in expense_transactions),
            "net_profit": sum(t.amount for t in income_transactions) - sum(t.amount for t in expense_transactions),
            "transaction_count": len(transactions),
            "income_count": len(income_transactions),
            "expense_count": len(expense_transactions),
            "avg_transaction_amount": sum(t.amount for t in transactions) / len(transactions) if transactions else 0
        }
        
        # Calculate health score
        health_score = health_scorer.calculate_score(financial_data, business_id, db)
        
        logger.info(f"Financial health score calculated for business {business_id}: {health_score['overall_score']}")
        
        return {
            "health_score": health_score
        }
        
    except Exception as e:
        logger.error(f"Financial health score calculation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate financial health score"
        )


# ========================================
# AI Agent Endpoints
# ========================================

@router.post("/agent/chat")
async def chat_with_ai_agent(
    message: str,
    language: str = "en",
    message_type: str = "text",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Interact with AI Financial Agent
    
    Chat with the autonomous AI agent for financial insights and recommendations.
    Supports text and voice inputs with multi-language support.
    
    - **message**: User message or question
    - **language**: Language code (en, hi, gu, mr, ta, te, bn, kn, ml, pa)
    - **message_type**: Type of message (text or voice)
    """
    
    try:
        business_id = current_user.business.id
        
        # Process message through AI agent
        agent_response = financial_agent.process_message(
            message=message,
            language=language,
            message_type=message_type,
            business_id=business_id,
            user_id=current_user.id,
            db=db
        )
        
        logger.info(f"AI agent chat processed for user {current_user.email}")
        
        return agent_response
        
    except Exception as e:
        logger.error(f"AI agent chat failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process AI agent chat"
        )


@router.post("/voice/insight")
async def get_voice_insight(
    audio_data: str,  # Base64 encoded audio
    language: str = "en",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get voice-based financial insights
    
    Process voice input and provide audio-visual financial insights.
    Uses Whisper AI for speech-to-text conversion.
    
    - **audio_data**: Base64 encoded audio data
    - **language**: Input language (default: en)
    """
    
    try:
        if not settings.enable_voice_features:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Voice features are disabled"
            )
        
        business_id = current_user.business.id
        
        # Decode base64 audio
        try:
            audio_bytes = base64.b64decode(audio_data)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid audio data format"
            )
        
        # Transcribe audio
        transcription_result = voice_service.transcribe_audio(
            audio_bytes=audio_bytes,
            language=language
        )
        
        if not transcription_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=transcription_result["error"]
            )
        
        # Process transcription through AI agent
        agent_response = financial_agent.process_message(
            message=transcription_result["text"],
            language=language,
            message_type="voice",
            business_id=business_id,
            user_id=current_user.id,
            db=db
        )
        
        # Generate audio response
        audio_response = voice_service.text_to_speech(
            text=agent_response["response"]["content"],
            language=language
        )
        
        logger.info(f"Voice insight processed for user {current_user.email}")
        
        return {
            "transcription": {
                "text": transcription_result["text"],
                "language": language,
                "confidence": transcription_result["confidence"]
            },
            "insight": {
                "type": "financial_query",
                "response_text": agent_response["response"]["content"],
                "response_audio_base64": audio_response["audio_base64"] if audio_response["success"] else None,
                "data": agent_response["response"].get("data"),
                "follow_up_actions": agent_response["response"].get("follow_up_actions")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Voice insight failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process voice insight"
        )


# ========================================
# Transaction Categorization Endpoints
# ========================================

@router.post("/categorize")
async def auto_categorize_transaction(
    description: str,
    transaction_type: str = "expense",
    current_user: User = Depends(get_current_user)
):
    """
    Auto-categorize transaction using NLP
    
    Automatically categorize a transaction based on its description using NLP.
    
    - **description**: Transaction description text
    - **transaction_type**: Type of transaction (income or expense)
    """
    
    try:
        if not settings.enable_auto_categorization:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Auto-categorization feature is disabled"
            )
        
        # Categorize transaction
        categorization_result = transaction_categorizer.categorize(
            description=description,
            transaction_type=transaction_type
        )
        
        return {
            "category": categorization_result["category"],
            "subcategory": categorization_result.get("subcategory"),
            "confidence": categorization_result["confidence"],
            "suggested_tags": categorization_result.get("suggested_tags", [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transaction categorization failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to categorize transaction"
        )


# ========================================
# Anomaly Detection Endpoints
# ========================================

@router.get("/anomalies")
async def detect_anomalies(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Detect financial anomalies
    
    Detect unusual transactions and patterns using ML-based anomaly detection.
    
    - **days**: Number of days to analyze (default: 30)
    """
    
    try:
        if not settings.enable_anomaly_detection:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Anomaly detection feature is disabled"
            )
        
        business_id = current_user.business.id
        
        # Get transactions for the specified period
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        transactions = db.query(Transaction).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).all()
        
        # Detect anomalies
        anomalies = []
        for transaction in transactions:
            # Check for amount anomalies (transactions 5x higher than average)
            avg_amount = sum(t.amount for t in transactions) / len(transactions)
            if transaction.amount > avg_amount * 5:
                anomalies.append({
                    "type": "amount_anomaly",
                    "severity": "high",
                    "transaction_id": str(transaction.id),
                    "message": f"Transaction amount ₹{transaction.amount} is 5x higher than average",
                    "transaction_date": transaction.transaction_date
                })
        
        logger.info(f"Anomaly detection completed for business {business_id}: {len(anomalies)} anomalies found")
        
        return {
            "period_days": days,
            "anomalies_detected": len(anomalies),
            "anomalies": anomalies
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Anomaly detection failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to detect anomalies"
        )


# ========================================
# Decision Support Endpoints
# ========================================

@router.get("/recommendations")
async def get_decision_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered decision recommendations
    
    Get actionable recommendations based on business performance analysis.
    Includes suggestions for cash management, inventory optimization, and growth strategies.
    """
    
    try:
        business_id = current_user.business.id
        
        # Get financial health score
        health_score = health_scorer.calculate_score(
            financial_data={},
            business_id=business_id,
            db=db
        )
        
        # Generate recommendations based on health score
        recommendations = []
        
        # Cash position recommendations
        if health_score["scores_breakdown"]["cash_position"]["score"] < 70:
            recommendations.append({
                "priority": "high",
                "category": "cash_position",
                "recommendation": "Improve cash position by reducing outstanding receivables",
                "expected_impact": "5-10% improvement in cash flow"
            })
        
        # Efficiency recommendations
        if health_score["scores_breakdown"]["efficiency"]["score"] < 70:
            recommendations.append({
                "priority": "medium",
                "category": "efficiency",
                "recommendation": "Optimize inventory levels to reduce carrying costs",
                "expected_impact": "3-5% reduction in storage costs"
            })
        
        # Growth recommendations
        if health_score["scores_breakdown"]["growth"]["score"] > 80:
            recommendations.append({
                "priority": "medium",
                "category": "growth",
                "recommendation": "Consider expanding product lines based on current growth trends",
                "expected_impact": "10-15% additional revenue potential"
            })
        
        logger.info(f"Decision recommendations generated for business {business_id}")
        
        return {
            "health_score": health_score["overall_score"],
            "health_category": health_score["category"],
            "recommendations": recommendations,
            "generated_at": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Decision recommendations failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recommendations"
        )


# ========================================
# Scenario Simulation Endpoints
# ========================================

@router.post("/simulate")
async def simulate_scenario(
    price_change: float = 0,
    demand_change: float = 0,
    marketing_spend: float = 0,
    duration_days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Simulate business scenarios (What-If Analysis)
    
    Simulate the impact of various business decisions on profitability.
    
    - **price_change**: Percentage change in price (e.g., 10 for +10%, -5 for -5%)
    - **demand_change**: Percentage change in demand (e.g., 15 for +15%, -10 for -10%)
    - **marketing_spend**: Additional marketing investment amount
    - **duration_days**: Duration of simulation in days
    """
    
    try:
        if not settings.enable_scenario_simulator:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Scenario simulator feature is disabled"
            )
        
        business_id = current_user.business.id
        
        # Get baseline financial data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=90)
        
        transactions = db.query(Transaction).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).all()
        
        # Calculate baseline metrics
        income_transactions = [t for t in transactions if t.transaction_type == "income"]
        expense_transactions = [t for t in transactions if t.transaction_type == "expense"]
        
        baseline_revenue = sum(t.amount for t in income_transactions)
        baseline_expenses = sum(t.amount for t in expense_transactions)
        baseline_profit = baseline_revenue - baseline_expenses
        
        # Calculate simulated metrics
        simulated_revenue = baseline_revenue * (1 + price_change / 100) * (1 + demand_change / 100)
        simulated_expenses = baseline_expenses + marketing_spend
        simulated_profit = simulated_revenue - simulated_expenses
        
        # Calculate impact
        revenue_change = ((simulated_revenue - baseline_revenue) / baseline_revenue * 100) if baseline_revenue > 0 else 0
        profit_change = ((simulated_profit - baseline_profit) / baseline_profit * 100) if baseline_profit > 0 else 0
        
        logger.info(f"Scenario simulation completed for business {business_id}")
        
        return {
            "scenario": {
                "price_change": price_change,
                "demand_change": demand_change,
                "marketing_spend": marketing_spend,
                "duration_days": duration_days
            },
            "baseline": {
                "revenue": baseline_revenue,
                "expenses": baseline_expenses,
                "profit": baseline_profit
            },
            "simulated": {
                "revenue": simulated_revenue,
                "expenses": simulated_expenses,
                "profit": simulated_profit
            },
            "impact": {
                "revenue_change": round(revenue_change, 2),
                "profit_change": round(profit_change, 2),
                "recommendation": self._get_simulation_recommendation(revenue_change, profit_change)
            },
            "generated_at": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Scenario simulation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to simulate scenario"
        )


def _get_simulation_recommendation(revenue_change: float, profit_change: float) -> str:
    """
    Get recommendation based on simulation results
    """
    if profit_change > 10:
        return "Strong positive impact. Proceed with this scenario."
    elif profit_change > 0:
        return "Positive impact. Consider implementing with caution."
    elif profit_change > -10:
        return "Minor negative impact. Review before implementing."
    else:
        return "Significant negative impact. Not recommended."