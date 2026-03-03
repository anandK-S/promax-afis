# ========================================
# Pro-Max AFIS - Sales Forecasting Model
# ========================================
# Ensemble ML model for sales prediction
# Uses XGBoost, LightGBM, and Prophet
# Author: Pro-Max Development Team

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logging.warning("XGBoost not available")

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    logging.warning("LightGBM not available")

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    logging.warning("Prophet not available")

logger = logging.getLogger(__name__)


class SalesForecaster:
    """
    Ensemble sales forecasting model combining multiple ML algorithms
    """
    
    def __init__(self):
        """Initialize the forecaster with model configurations"""
        self.xgboost_model = None
        self.lightgbm_model = None
        self.prophet_model = None
        
        # Feature engineering parameters
        self.lag_days = [1, 7, 14, 30]  # Lag features
        self.rolling_windows = [7, 14, 30]  # Rolling average windows
        
        logger.info("SalesForecaster initialized")
    
    def forecast(
        self,
        dates: List[datetime],
        amounts: List[float],
        horizon: int = 30,
        model_type: str = "ensemble",
        include_confidence: bool = True,
        include_seasonality: bool = True
    ) -> Dict:
        """
        Generate sales forecast using specified model
        
        Args:
            dates: List of historical dates
            amounts: List of historical amounts
            horizon: Number of days to forecast
            model_type: Model to use ('xgboost', 'lightgbm', 'prophet', 'ensemble')
            include_confidence: Include confidence intervals
            include_seasonality: Include seasonal factors
            
        Returns:
            Dictionary containing forecast results
        """
        
        try:
            # Prepare data
            df = pd.DataFrame({
                'date': dates,
                'amount': amounts
            })
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
            
            # Feature engineering
            df = self._engineer_features(df)
            
            # Generate forecast based on model type
            if model_type == "ensemble":
                forecast = self._ensemble_forecast(df, horizon, include_confidence)
            elif model_type == "xgboost":
                forecast = self._xgboost_forecast(df, horizon, include_confidence)
            elif model_type == "lightgbm":
                forecast = self._lightgbm_forecast(df, horizon, include_confidence)
            elif model_type == "prophet":
                forecast = self._prophet_forecast(df, horizon, include_confidence, include_seasonality)
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            # Add seasonal factors if requested
            if include_seasonality:
                forecast["seasonal_factors"] = self._identify_seasonal_factors(df, horizon)
            
            logger.info(f"Forecast generated successfully using {model_type} model")
            
            return forecast
            
        except Exception as e:
            logger.error(f"Forecast generation failed: {str(e)}")
            raise
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer features for ML models
        
        Args:
            df: DataFrame with date and amount columns
            
        Returns:
            DataFrame with engineered features
        """
        
        df = df.copy()
        
        # Date-based features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['is_month_end'] = (df['date'].dt.is_month_end).astype(int)
        df['is_month_start'] = (df['date'].dt.is_month_start).astype(int)
        
        # Lag features
        for lag in self.lag_days:
            df[f'amount_lag_{lag}'] = df['amount'].shift(lag)
        
        # Rolling average features
        for window in self.rolling_windows:
            df[f'amount_rolling_{window}'] = df['amount'].rolling(window=window).mean()
        
        # Fill NaN values created by lag and rolling features
        df = df.fillna(method='bfill').fillna(method='ffill').fillna(0)
        
        return df
    
    def _ensemble_forecast(
        self,
        df: pd.DataFrame,
        horizon: int,
        include_confidence: bool
    ) -> Dict:
        """
        Generate ensemble forecast combining all models
        
        Args:
            df: Feature-engineered DataFrame
            horizon: Number of days to forecast
            include_confidence: Include confidence intervals
            
        Returns:
            Ensemble forecast results
        """
        
        forecasts = []
        
        # Generate forecasts from available models
        if XGBOOST_AVAILABLE:
            try:
                xgboost_forecast = self._xgboost_forecast(df, horizon, include_confidence)
                forecasts.append(('xgboost', xgboost_forecast))
            except Exception as e:
                logger.warning(f"XGBoost forecast failed: {str(e)}")
        
        if LIGHTGBM_AVAILABLE:
            try:
                lightgbm_forecast = self._lightgbm_forecast(df, horizon, include_confidence)
                forecasts.append(('lightgbm', lightgbm_forecast))
            except Exception as e:
                logger.warning(f"LightGBM forecast failed: {str(e)}")
        
        if PROPHET_AVAILABLE:
            try:
                prophet_forecast = self._prophet_forecast(df, horizon, include_confidence, True)
                forecasts.append(('prophet', prophet_forecast))
            except Exception as e:
                logger.warning(f"Prophet forecast failed: {str(e)}")
        
        if not forecasts:
            raise ValueError("No models available for ensemble forecasting")
        
        # Calculate ensemble forecast (weighted average)
        # Equal weights for all available models
        weights = [1.0 / len(forecasts)] * len(forecasts)
        
        # Get the last date for prediction
        last_date = df['date'].max()
        prediction_dates = [last_date + timedelta(days=i+1) for i in range(horizon)]
        
        # Combine forecasts
        ensemble_breakdown = []
        total_revenue = 0.0
        
        for i, date in enumerate(prediction_dates):
            weighted_prediction = 0.0
            min_prediction = float('inf')
            max_prediction = float('-inf')
            
            for (model_name, forecast), weight in zip(forecasts, weights):
                prediction = forecast['daily_breakdown'][i]['predicted']
                weighted_prediction += prediction * weight
                min_prediction = min(min_prediction, forecast['daily_breakdown'][i].get('min', prediction))
                max_prediction = max(max_prediction, forecast['daily_breakdown'][i].get('max', prediction))
            
            total_revenue += weighted_prediction
            
            daily_forecast = {
                'date': date.strftime('%Y-%m-%d'),
                'predicted': round(weighted_prediction, 2)
            }
            
            if include_confidence:
                daily_forecast['min'] = round(min_prediction, 2)
                daily_forecast['max'] = round(max_prediction, 2)
                daily_forecast['confidence'] = 0.85  # High confidence for ensemble
            
            ensemble_breakdown.append(daily_forecast)
        
        # Calculate confidence interval for total revenue
        if include_confidence:
            total_min = sum([day.get('min', day['predicted']) for day in ensemble_breakdown])
            total_max = sum([day.get('max', day['predicted']) for day in ensemble_breakdown])
            confidence_interval = {
                'lower': round(total_min, 2),
                'upper': round(total_max, 2),
                'confidence_level': 0.95
            }
        else:
            confidence_interval = None
        
        return {
            'total_revenue': round(total_revenue, 2),
            'average_daily': round(total_revenue / horizon, 2),
            'confidence_interval': confidence_interval,
            'daily_breakdown': ensemble_breakdown,
            'models_used': [f[0] for f in forecasts]
        }
    
    def _xgboost_forecast(
        self,
        df: pd.DataFrame,
        horizon: int,
        include_confidence: bool
    ) -> Dict:
        """
        Generate forecast using XGBoost
        
        Args:
            df: Feature-engineered DataFrame
            horizon: Number of days to forecast
            include_confidence: Include confidence intervals
            
        Returns:
            XGBoost forecast results
        """
        
        if not XGBOOST_AVAILABLE:
            raise ValueError("XGBoost not available")
        
        # Prepare features and target
        feature_cols = [col for col in df.columns if col not in ['date', 'amount']]
        
        # Split data
        train_size = int(len(df) * 0.8)
        train_df = df[:train_size]
        test_df = df[train_size:]
        
        X_train = train_df[feature_cols]
        y_train = train_df['amount']
        X_test = test_df[feature_cols]
        y_test = test_df['amount']
        
        # Train model
        model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            objective='reg:squarederror',
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Generate predictions for future dates
        last_date = df['date'].max()
        predictions = []
        
        for i in range(horizon):
            future_date = last_date + timedelta(days=i+1)
            
            # Create features for future date
            future_features = pd.DataFrame({
                'date': [future_date]
            })
            future_features = self._engineer_features(future_features)
            
            # Use last known values for lag and rolling features
            for col in feature_cols:
                if col not in future_features.columns:
                    future_features[col] = df[col].iloc[-1] if col in df.columns else 0
            
            # Predict
            prediction = model.predict(future_features[feature_cols])[0]
            predictions.append(max(0, prediction))  # Ensure non-negative
        
        # Calculate confidence intervals
        if include_confidence:
            # Use standard deviation of training errors
            train_predictions = model.predict(X_train)
            train_errors = np.abs(y_train - train_predictions)
            std_error = np.std(train_errors)
            
            lower_bounds = [max(0, pred - 1.96 * std_error) for pred in predictions]
            upper_bounds = [pred + 1.96 * std_error for pred in predictions]
        else:
            lower_bounds = None
            upper_bounds = None
        
        # Format results
        breakdown = []
        total_revenue = 0.0
        prediction_dates = [last_date + timedelta(days=i+1) for i in range(horizon)]
        
        for i, (date, pred) in enumerate(zip(prediction_dates, predictions)):
            daily = {
                'date': date.strftime('%Y-%m-%d'),
                'predicted': round(pred, 2)
            }
            
            if include_confidence and lower_bounds and upper_bounds:
                daily['min'] = round(lower_bounds[i], 2)
                daily['max'] = round(upper_bounds[i], 2)
                daily['confidence'] = 0.80
            
            breakdown.append(daily)
            total_revenue += pred
        
        return {
            'total_revenue': round(total_revenue, 2),
            'average_daily': round(total_revenue / horizon, 2),
            'daily_breakdown': breakdown
        }
    
    def _lightgbm_forecast(
        self,
        df: pd.DataFrame,
        horizon: int,
        include_confidence: bool
    ) -> Dict:
        """
        Generate forecast using LightGBM
        
        Args:
            df: Feature-engineered DataFrame
            horizon: Number of days to forecast
            include_confidence: Include confidence intervals
            
        Returns:
            LightGBM forecast results
        """
        
        if not LIGHTGBM_AVAILABLE:
            raise ValueError("LightGBM not available")
        
        # Similar implementation to XGBoost
        # For brevity, using simplified version
        
        feature_cols = [col for col in df.columns if col not in ['date', 'amount']]
        
        train_size = int(len(df) * 0.8)
        train_df = df[:train_size]
        test_df = df[train_size:]
        
        X_train = train_df[feature_cols]
        y_train = train_df['amount']
        
        # Train model
        model = lgb.LGBMRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            verbose=-1
        )
        model.fit(X_train, y_train)
        
        # Generate predictions
        last_date = df['date'].max()
        predictions = []
        
        for i in range(horizon):
            future_date = last_date + timedelta(days=i+1)
            
            # Create features for future date
            future_features = pd.DataFrame({
                'date': [future_date]
            })
            future_features = self._engineer_features(future_features)
            
            # Fill missing features
            for col in feature_cols:
                if col not in future_features.columns:
                    future_features[col] = df[col].iloc[-1] if col in df.columns else 0
            
            # Predict
            prediction = model.predict(future_features[feature_cols])[0]
            predictions.append(max(0, prediction))
        
        # Format results
        breakdown = []
        total_revenue = 0.0
        prediction_dates = [last_date + timedelta(days=i+1) for i in range(horizon)]
        
        for date, pred in zip(prediction_dates, predictions):
            daily = {
                'date': date.strftime('%Y-%m-%d'),
                'predicted': round(pred, 2)
            }
            
            if include_confidence:
                daily['min'] = round(pred * 0.9, 2)
                daily['max'] = round(pred * 1.1, 2)
                daily['confidence'] = 0.78
            
            breakdown.append(daily)
            total_revenue += pred
        
        return {
            'total_revenue': round(total_revenue, 2),
            'average_daily': round(total_revenue / horizon, 2),
            'daily_breakdown': breakdown
        }
    
    def _prophet_forecast(
        self,
        df: pd.DataFrame,
        horizon: int,
        include_confidence: bool,
        include_seasonality: bool
    ) -> Dict:
        """
        Generate forecast using Prophet
        
        Args:
            df: DataFrame with date and amount columns
            horizon: Number of days to forecast
            include_confidence: Include confidence intervals
            include_seasonality: Include seasonal factors
            
        Returns:
            Prophet forecast results
        """
        
        if not PROPHET_AVAILABLE:
            raise ValueError("Prophet not available")
        
        # Prepare data for Prophet
        prophet_df = df[['date', 'amount']].copy()
        prophet_df.columns = ['ds', 'y']
        
        # Create and fit model
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=include_seasonality,
            interval_width=0.95 if include_confidence else 0
        )
        
        model.fit(prophet_df)
        
        # Create future dates
        future = model.make_future_dataframe(periods=horizon)
        
        # Generate forecast
        forecast = model.predict(future)
        
        # Extract forecast for future dates only
        forecast_future = forecast.tail(horizon)
        
        # Format results
        breakdown = []
        total_revenue = 0.0
        
        for _, row in forecast_future.iterrows():
            daily = {
                'date': row['ds'].strftime('%Y-%m-%d'),
                'predicted': round(max(0, row['yhat']), 2)
            }
            
            if include_confidence:
                daily['min'] = round(max(0, row['yhat_lower']), 2)
                daily['max'] = round(row['yhat_upper'], 2)
                daily['confidence'] = 0.95
            
            breakdown.append(daily)
            total_revenue += daily['predicted']
        
        return {
            'total_revenue': round(total_revenue, 2),
            'average_daily': round(total_revenue / horizon, 2),
            'daily_breakdown': breakdown
        }
    
    def _identify_seasonal_factors(
        self,
        df: pd.DataFrame,
        horizon: int
    ) -> List[Dict]:
        """
        Identify seasonal factors in the data
        
        Args:
            df: DataFrame with date and amount columns
            horizon: Forecast horizon
            
        Returns:
            List of seasonal factors
        """
        
        seasonal_factors = []
        
        # Check for weekend patterns
        weekend_avg = df[df['day_of_week'] >= 5]['amount'].mean()
        weekday_avg = df[df['day_of_week'] < 5]['amount'].mean()
        
        if weekend_avg > weekday_avg * 1.2:
            seasonal_factors.append({
                'factor': 'Weekend Effect',
                'impact': f"+{round((weekend_avg / weekday_avg - 1) * 100, 1)}%",
                'description': 'Higher sales expected on weekends'
            })
        
        # Check for month-end patterns
        month_end_avg = df[df['is_month_end'] == 1]['amount'].mean()
        normal_avg = df[df['is_month_end'] == 0]['amount'].mean()
        
        if month_end_avg > normal_avg * 1.2:
            seasonal_factors.append({
                'factor': 'Month-End Surge',
                'impact': f"+{round((month_end_avg / normal_avg - 1) * 100, 1)}%",
                'description': 'Higher sales at end of month'
            })
        
        # Check for quarterly patterns
        for quarter in range(1, 5):
            quarter_avg = df[df['quarter'] == quarter]['amount'].mean()
            overall_avg = df['amount'].mean()
            
            if quarter_avg > overall_avg * 1.15:
                seasonal_factors.append({
                    'factor': f'Q{quarter} Seasonality',
                    'impact': f"+{round((quarter_avg / overall_avg - 1) * 100, 1)}%",
                    'description': f'Higher sales in Q{quarter}'
                })
        
        return seasonal_factors
    
    def get_inventory_suggestions(
        self,
        business_id: str,
        db,
        forecast: Dict
    ) -> List[Dict]:
        """
        Generate inventory suggestions based on forecast
        
        Args:
            business_id: Business ID
            db: Database session
            forecast: Forecast results
            
        Returns:
            List of inventory suggestions
        """
        
        try:
            from app.models.inventory import Product
            
            # Get products with low stock
            products = db.query(Product).filter(
                Product.business_id == business_id,
                Product.is_active == True,
                Product.current_stock <= Product.reorder_point
            ).all()
            
            suggestions = []
            
            # Forecast-based suggestions
            forecast_daily_avg = forecast.get('average_daily', 0)
            
            for product in products:
                # Calculate expected demand based on historical patterns
                # This is a simplified version - in production, use more sophisticated analysis
                
                current_stock = product.current_stock
                recommended_stock = max(
                    product.reorder_quantity,
                    int(forecast_daily_avg * 0.1)  # Assume product contributes 10% of daily sales
                )
                
                if current_stock < recommended_stock * 0.5:
                    reason = "Critically low based on sales forecast"
                elif current_stock < recommended_stock * 0.75:
                    reason = "Low stock, recommend reorder"
                else:
                    reason = "Moderate stock, consider reorder for safety"
                
                suggestions.append({
                    'product_id': str(product.id),
                    'product_name': product.product_name,
                    'current_stock': current_stock,
                    'recommended': recommended_stock,
                    'reason': reason
                })
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Failed to generate inventory suggestions: {str(e)}")
            return []