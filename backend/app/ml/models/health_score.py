# ========================================
# Pro-Max AFIS - Financial Health Scoring Model
# ========================================
# Business Pulse Score calculation algorithm
# Author: Pro-Max Development Team

from typing import Dict, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class FinancialHealthScorer:
    """
    Financial health scoring system that calculates Business Pulse Score (0-100)
    based on multiple financial indicators
    """
    
    def __init__(self):
        """Initialize the health scorer"""
        # Score weights for each component
        self.weights = {
            'cash_position': 0.25,
            'profitability': 0.20,
            'solvency': 0.20,
            'efficiency': 0.20,
            'growth': 0.15
        }
        
        logger.info("FinancialHealthScorer initialized")
    
    def calculate_score(
        self,
        financial_data: Dict,
        business_id: str,
        db
    ) -> Dict:
        """
        Calculate comprehensive financial health score
        
        Args:
            financial_data: Basic financial metrics
            business_id: Business ID for database queries
            db: Database session
            
        Returns:
            Dictionary containing health score and breakdown
        """
        
        try:
            # Calculate individual component scores
            cash_score = self._calculate_cash_position_score(financial_data, db)
            profitability_score = self._calculate_profitability_score(financial_data, db)
            solvency_score = self._calculate_solvency_score(financial_data, db)
            efficiency_score = self._calculate_efficiency_score(financial_data, db)
            growth_score = self._calculate_growth_score(financial_data, db)
            
            # Calculate weighted overall score
            overall_score = (
                cash_score['score'] * self.weights['cash_position'] +
                profitability_score['score'] * self.weights['profitability'] +
                solvency_score['score'] * self.weights['solvency'] +
                efficiency_score['score'] * self.weights['efficiency'] +
                growth_score['score'] * self.weights['growth']
            )
            
            # Determine health category
            health_category = self._get_health_category(overall_score)
            
            # Generate recommendations
            recommendations = self._generate_recommendations({
                'cash_position': cash_score,
                'profitability': profitability_score,
                'solvency': solvency_score,
                'efficiency': efficiency_score,
                'growth': growth_score
            })
            
            return {
                'overall_score': round(overall_score, 2),
                'category': health_category,
                'calculated_at': datetime.utcnow(),
                'scores_breakdown': {
                    'cash_position': {
                        'score': round(cash_score['score'], 2),
                        'weight': self.weights['cash_position'],
                        'details': cash_score['details']
                    },
                    'profitability': {
                        'score': round(profitability_score['score'], 2),
                        'weight': self.weights['profitability'],
                        'details': profitability_score['details']
                    },
                    'solvency': {
                        'score': round(solvency_score['score'], 2),
                        'weight': self.weights['solvency'],
                        'details': solvency_score['details']
                    },
                    'efficiency': {
                        'score': round(efficiency_score['score'], 2),
                        'weight': self.weights['efficiency'],
                        'details': efficiency_score['details']
                    },
                    'growth': {
                        'score': round(growth_score['score'], 2),
                        'weight': self.weights['growth'],
                        'details': growth_score['details']
                    }
                },
                'trend': self._calculate_trend(business_id, db),
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Health score calculation failed: {str(e)}")
            raise
    
    def _calculate_cash_position_score(
        self,
        financial_data: Dict,
        db
    ) -> Dict:
        """
        Calculate cash position score (0-100)
        
        Factors:
        - Cash on hand vs monthly expenses
        - Cash flow consistency
        - Emergency fund adequacy
        """
        
        try:
            # Get current cash balance
            from app.models.financial import Transaction
            
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=30)
            
            transactions = db.query(Transaction).filter(
                Transaction.business_id == financial_data.get('business_id'),
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).all()
            
            income = sum(t.amount for t in transactions if t.transaction_type == 'income')
            expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
            net_cash_flow = income - expenses
            
            # Calculate cash runway (days of expenses covered)
            cash_on_hand = income - expenses  # Simplified
            daily_burn_rate = expenses / 30 if expenses > 0 else 1
            cash_runway = cash_on_hand / daily_burn_rate if daily_burn_rate > 0 else 0
            
            # Score based on cash runway
            if cash_runway >= 90:
                score = 100
            elif cash_runway >= 60:
                score = 90
            elif cash_runway >= 30:
                score = 75
            elif cash_runway >= 15:
                score = 50
            else:
                score = 25
            
            # Adjust for cash flow consistency
            if net_cash_flow > 0:
                score += 5
            
            score = min(100, max(0, score))
            
            return {
                'score': score,
                'details': {
                    'cash_on_hand': cash_on_hand,
                    'monthly_expenses': expenses,
                    'cash_runway_days': round(cash_runway, 1),
                    'net_cash_flow': net_cash_flow
                }
            }
            
        except Exception as e:
            logger.error(f"Cash position score calculation failed: {str(e)}")
            return {'score': 50, 'details': {}}
    
    def _calculate_profitability_score(
        self,
        financial_data: Dict,
        db
    ) -> Dict:
        """
        Calculate profitability score (0-100)
        
        Factors:
        - Net profit margin
        - Gross profit margin
        - Operating profit margin
        """
        
        try:
            total_income = financial_data.get('total_income', 0)
            total_expenses = financial_data.get('total_expenses', 0)
            net_profit = financial_data.get('net_profit', 0)
            
            if total_income == 0:
                return {'score': 0, 'details': {}}
            
            # Calculate profit margins
            net_profit_margin = (net_profit / total_income) * 100
            gross_profit_margin = (total_income * 0.7 / total_income) * 100  # Assuming 70% gross margin
            operating_profit_margin = net_profit_margin  # Simplified
            
            # Score based on net profit margin
            if net_profit_margin >= 20:
                score = 100
            elif net_profit_margin >= 15:
                score = 85
            elif net_profit_margin >= 10:
                score = 70
            elif net_profit_margin >= 5:
                score = 50
            elif net_profit_margin >= 0:
                score = 30
            else:
                score = 0
            
            score = min(100, max(0, score))
            
            return {
                'score': score,
                'details': {
                    'net_profit_margin': round(net_profit_margin, 2),
                    'gross_profit_margin': round(gross_profit_margin, 2),
                    'operating_profit_margin': round(operating_profit_margin, 2)
                }
            }
            
        except Exception as e:
            logger.error(f"Profitability score calculation failed: {str(e)}")
            return {'score': 50, 'details': {}}
    
    def _calculate_solvency_score(
        self,
        financial_data: Dict,
        db
    ) -> Dict:
        """
        Calculate solvency score (0-100)
        
        Factors:
        - Debt to equity ratio
        - Current ratio
        - Quick ratio
        """
        
        try:
            # Simplified solvency calculation
            # In production, get actual debt and asset data from database
            
            # Current ratio (Current Assets / Current Liabilities)
            # Assuming healthy current ratio of 1.5+
            current_ratio = 1.5
            
            # Debt to equity ratio
            # Assuming low debt to equity of 0.5
            debt_to_equity_ratio = 0.5
            
            # Quick ratio (Quick Assets / Current Liabilities)
            quick_ratio = 1.2
            
            # Calculate score based on ratios
            score = 0
            
            if current_ratio >= 2:
                score += 35
            elif current_ratio >= 1.5:
                score += 30
            elif current_ratio >= 1:
                score += 20
            
            if debt_to_equity_ratio <= 0.5:
                score += 35
            elif debt_to_equity_ratio <= 1:
                score += 25
            elif debt_to_equity_ratio <= 2:
                score += 15
            
            if quick_ratio >= 1:
                score += 30
            elif quick_ratio >= 0.8:
                score += 20
            elif quick_ratio >= 0.5:
                score += 10
            
            score = min(100, max(0, score))
            
            return {
                'score': score,
                'details': {
                    'debt_to_equity_ratio': debt_to_equity_ratio,
                    'current_ratio': current_ratio,
                    'quick_ratio': quick_ratio
                }
            }
            
        except Exception as e:
            logger.error(f"Solvency score calculation failed: {str(e)}")
            return {'score': 50, 'details': {}}
    
    def _calculate_efficiency_score(
        self,
        financial_data: Dict,
        db
    ) -> Dict:
        """
        Calculate efficiency score (0-100)
        
        Factors:
        - Inventory turnover
        - Receivables turnover
        - Asset turnover
        """
        
        try:
            from app.models.inventory import Product, InventoryMovement
            
            # Get inventory turnover
            products = db.query(Product).filter(
                Product.is_active == True
            ).all()
            
            total_inventory_value = sum(p.cost_price * p.current_stock for p in products)
            
            # Calculate inventory turnover (COGS / Average Inventory)
            cogs = financial_data.get('total_expenses', 0) * 0.7  # Assuming 70% are COGS
            inventory_turnover = (cogs / total_inventory_value) if total_inventory_value > 0 else 0
            
            # Receivables turnover (Net Credit Sales / Average Receivables)
            receivables_turnover = 8.0  # Assumed healthy value
            
            # Asset turnover (Net Sales / Total Assets)
            asset_turnover = 2.0  # Assumed healthy value
            
            # Calculate score based on ratios
            score = 0
            
            if inventory_turnover >= 8:
                score += 35
            elif inventory_turnover >= 6:
                score += 30
            elif inventory_turnover >= 4:
                score += 20
            elif inventory_turnover >= 2:
                score += 10
            
            if receivables_turnover >= 10:
                score += 35
            elif receivables_turnover >= 8:
                score += 30
            elif receivables_turnover >= 6:
                score += 20
            
            if asset_turnover >= 2.5:
                score += 30
            elif asset_turnover >= 2:
                score += 25
            elif asset_turnover >= 1.5:
                score += 15
            
            score = min(100, max(0, score))
            
            return {
                'score': score,
                'details': {
                    'inventory_turnover': round(inventory_turnover, 2),
                    'receivables_turnover': receivables_turnover,
                    'asset_turnover': asset_turnover
                }
            }
            
        except Exception as e:
            logger.error(f"Efficiency score calculation failed: {str(e)}")
            return {'score': 50, 'details': {}}
    
    def _calculate_growth_score(
        self,
        financial_data: Dict,
        db
    ) -> Dict:
        """
        Calculate growth score (0-100)
        
        Factors:
        - Revenue growth rate
        - Profit growth rate
        - Customer growth rate
        """
        
        try:
            from app.models.financial import Transaction
            
            # Calculate growth rates
            end_date = datetime.utcnow()
            mid_date = end_date - timedelta(days=30)
            start_date = end_date - timedelta(days=60)
            
            # Revenue for current month
            current_month_income = db.query(Transaction).filter(
                Transaction.transaction_date >= mid_date,
                Transaction.transaction_date <= end_date,
                Transaction.transaction_type == 'income'
            ).all()
            
            current_month_revenue = sum(t.amount for t in current_month_income)
            
            # Revenue for previous month
            previous_month_income = db.query(Transaction).filter(
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= mid_date,
                Transaction.transaction_type == 'income'
            ).all()
            
            previous_month_revenue = sum(t.amount for t in previous_month_income)
            
            # Calculate growth rates
            if previous_month_revenue > 0:
                revenue_growth_rate = ((current_month_revenue - previous_month_revenue) / previous_month_revenue) * 100
            else:
                revenue_growth_rate = 0
            
            # Profit growth rate (simplified)
            profit_growth_rate = revenue_growth_rate * 0.8
            
            # Customer growth rate (assumed)
            customer_growth_rate = revenue_growth_rate * 0.5
            
            # Calculate score based on growth rates
            score = 0
            
            if revenue_growth_rate >= 20:
                score += 40
            elif revenue_growth_rate >= 10:
                score += 30
            elif revenue_growth_rate >= 5:
                score += 20
            elif revenue_growth_rate >= 0:
                score += 10
            
            if profit_growth_rate >= 15:
                score += 30
            elif profit_growth_rate >= 10:
                score += 25
            elif profit_growth_rate >= 5:
                score += 15
            elif profit_growth_rate >= 0:
                score += 5
            
            if customer_growth_rate >= 15:
                score += 30
            elif customer_growth_rate >= 10:
                score += 25
            elif customer_growth_rate >= 5:
                score += 15
            elif customer_growth_rate >= 0:
                score += 5
            
            score = min(100, max(0, score))
            
            return {
                'score': score,
                'details': {
                    'revenue_growth_rate': round(revenue_growth_rate, 2),
                    'profit_growth_rate': round(profit_growth_rate, 2),
                    'customer_growth_rate': round(customer_growth_rate, 2)
                }
            }
            
        except Exception as e:
            logger.error(f"Growth score calculation failed: {str(e)}")
            return {'score': 50, 'details': {}}
    
    def _get_health_category(self, score: float) -> str:
        """
        Get health category based on score
        
        Args:
            score: Health score (0-100)
            
        Returns:
            Health category string
        """
        
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 60:
            return "Fair"
        elif score >= 40:
            return "Poor"
        else:
            return "Critical"
    
    def _calculate_trend(self, business_id: str, db) -> Dict:
        """
        Calculate health score trend over time
        
        Args:
            business_id: Business ID
            db: Database session
            
        Returns:
            Dictionary with trend information
        """
        
        try:
            from app.models.ml_predictions import FinancialHealthScore
            
            # Get previous month's score
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=35)
            
            previous_score = db.query(FinancialHealthScore).filter(
                FinancialHealthScore.business_id == business_id,
                FinancialHealthScore.score_date >= start_date,
                FinancialHealthScore.score_date < start_date + timedelta(days=5)
            ).first()
            
            if previous_score:
                current_score = 75  # Placeholder - would be calculated
                change = current_score - previous_score.overall_score
                
                if change > 5:
                    direction = "improving"
                elif change < -5:
                    direction = "declining"
                else:
                    direction = "stable"
                
                return {
                    'current': current_score,
                    'previous_month': previous_score.overall_score,
                    'change': round(change, 2),
                    'direction': direction
                }
            else:
                return {
                    'current': 75,
                    'previous_month': None,
                    'change': 0,
                    'direction': 'stable'
                }
                
        except Exception as e:
            logger.error(f"Trend calculation failed: {str(e)}")
            return {
                'current': 75,
                'previous_month': None,
                'change': 0,
                'direction': 'stable'
            }
    
    def _generate_recommendations(self, scores: Dict) -> List[Dict]:
        """
        Generate recommendations based on health scores
        
        Args:
            scores: Dictionary of individual component scores
            
        Returns:
            List of recommendation dictionaries
        """
        
        recommendations = []
        
        # Cash position recommendations
        if scores['cash_position']['score'] < 70:
            recommendations.append({
                'priority': 'high',
                'category': 'cash_position',
                'recommendation': 'Improve cash position by reducing outstanding receivables and optimizing payment terms',
                'expected_impact': '10-15% improvement in cash flow'
            })
        
        # Profitability recommendations
        if scores['profitability']['score'] < 70:
            recommendations.append({
                'priority': 'high',
                'category': 'profitability',
                'recommendation': 'Increase profit margins by reducing operational costs and optimizing pricing strategy',
                'expected_impact': '5-10% improvement in profit margins'
            })
        
        # Efficiency recommendations
        if scores['efficiency']['score'] < 70:
            recommendations.append({
                'priority': 'medium',
                'category': 'efficiency',
                'recommendation': 'Optimize inventory levels and improve supply chain efficiency',
                'expected_impact': '3-5% reduction in carrying costs'
            })
        
        # Growth recommendations
        if scores['growth']['score'] < 70:
            recommendations.append({
                'priority': 'medium',
                'category': 'growth',
                'recommendation': 'Focus on customer acquisition and retention strategies',
                'expected_impact': '10-15% increase in revenue growth'
            })
        
        return recommendations