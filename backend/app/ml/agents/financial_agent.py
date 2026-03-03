# ========================================
# Pro-Max AFIS - AI Financial Agent
# ========================================
# Autonomous AI agent for financial intelligence
# Author: Pro-Max Development Team

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FinancialAgent:
    """
    Autonomous AI Financial Agent that provides proactive insights,
    recommendations, and answers financial queries
    """
    
    def __init__(self):
        """Initialize the financial agent"""
        
        # Intent classification patterns
        self.intents = {
            'profit_query': ['profit', 'munafa', 'earning', 'income'],
            'expense_query': ['expense', 'kharch', 'cost', 'spending'],
            'sales_query': ['sales', 'sale', 'revenue', 'business'],
            'inventory_query': ['inventory', 'stock', 'product', 'stock level'],
            'cash_query': ['cash', 'balance', 'money', 'fund'],
            'forecast_request': ['forecast', 'predict', 'future', 'prediction'],
            'health_query': ['health', 'score', 'status', 'performance']
        }
        
        # Action buttons for quick access
        self.action_buttons = [
            {
                "action": "predict_next_month_sales",
                "label": "Predict next month's sales",
                "icon": "📈"
            },
            {
                "action": "analyze_top_expenses",
                "label": "Analyze my top 3 expenses",
                "icon": "💸"
            },
            {
                "action": "check_inventory_status",
                "label": "Check inventory status",
                "icon": "📦"
            },
            {
                "action": "get_financial_health",
                "label": "Get financial health score",
                "icon": "💓"
            }
        ]
        
        logger.info("FinancialAgent initialized")
    
    def process_message(
        self,
        message: str,
        language: str = "en",
        message_type: str = "text",
        business_id: str = "",
        user_id: str = "",
        db = None
    ) -> Dict:
        """
        Process user message and generate AI response
        
        Args:
            message: User's message or query
            language: Language code (en, hi, gu, mr, etc.)
            message_type: Type of message (text or voice)
            business_id: Business ID
            user_id: User ID
            db: Database session
            
        Returns:
            Dictionary containing AI response
        """
        
        try:
            # Detect intent
            intent = self._detect_intent(message)
            
            # Extract entities
            entities = self._extract_entities(message)
            
            # Generate response based on intent
            response = self._generate_response(intent, entities, business_id, db, language)
            
            logger.info(f"AI agent processed message: intent={intent}, language={language}")
            
            return {
                "conversation_id": f"conv_{datetime.utcnow().timestamp()}",
                "response": response,
                "intent_detected": intent,
                "entities_extracted": entities
            }
            
        except Exception as e:
            logger.error(f"AI agent processing failed: {str(e)}")
            return {
                "conversation_id": f"conv_{datetime.utcnow().timestamp()}",
                "response": {
                    "type": "text",
                    "content": self._get_error_message(language),
                    "language": language
                },
                "intent_detected": "unknown",
                "entities_extracted": {}
            }
    
    def _detect_intent(self, message: str) -> str:
        """
        Detect the intent of the user's message
        
        Args:
            message: User's message
            
        Returns:
            Detected intent string
        """
        
        message_lower = message.lower()
        
        for intent, keywords in self.intents.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        
        return "general_query"
    
    def _extract_entities(self, message: str) -> Dict:
        """
        Extract entities from the user's message
        
        Args:
            message: User's message
            
        Returns:
            Dictionary of extracted entities
        """
        
        entities = {}
        message_lower = message.lower()
        
        # Extract time period
        time_keywords = {
            'today': 'today',
            'aaj': 'today',
            'kal': 'tomorrow',
            'tomorrow': 'tomorrow',
            'week': 'week',
            'month': 'month',
            'year': 'year'
        }
        
        for keyword, entity_value in time_keywords.items():
            if keyword in message_lower:
                entities['time_period'] = entity_value
                break
        
        # Extract metric type
        metric_keywords = {
            'profit': 'profit',
            'munafa': 'profit',
            'sales': 'sales',
            'revenue': 'sales',
            'expense': 'expense',
            'kharch': 'expense',
            'cash': 'cash',
            'inventory': 'inventory'
        }
        
        for keyword, entity_value in metric_keywords.items():
            if keyword in message_lower:
                entities['metric'] = entity_value
                break
        
        return entities
    
    def _generate_response(
        self,
        intent: str,
        entities: Dict,
        business_id: str,
        db,
        language: str
    ) -> Dict:
        """
        Generate response based on detected intent
        
        Args:
            intent: Detected intent
            entities: Extracted entities
            business_id: Business ID
            db: Database session
            language: Response language
            
        Returns:
            Response dictionary
        """
        
        try:
            if intent == "profit_query":
                return self._generate_profit_response(entities, business_id, db, language)
            elif intent == "expense_query":
                return self._generate_expense_response(entities, business_id, db, language)
            elif intent == "sales_query":
                return self._generate_sales_response(entities, business_id, db, language)
            elif intent == "inventory_query":
                return self._generate_inventory_response(entities, business_id, db, language)
            elif intent == "cash_query":
                return self._generate_cash_response(entities, business_id, db, language)
            elif intent == "health_query":
                return self._generate_health_response(entities, business_id, db, language)
            else:
                return self._generate_general_response(language)
                
        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}")
            return self._generate_general_response(language)
    
    def _generate_profit_response(
        self,
        entities: Dict,
        business_id: str,
        db,
        language: str
    ) -> Dict:
        """
        Generate profit query response
        """
        
        try:
            from app.models.financial import Transaction
            
            # Get today's profit
            end_date = datetime.utcnow()
            start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
            
            transactions = db.query(Transaction).filter(
                Transaction.business_id == business_id,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).all()
            
            income = sum(t.amount for t in transactions if t.transaction_type == 'income')
            expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
            profit = income - expenses
            
            # Get yesterday's profit for comparison
            yesterday_start = start_date - timedelta(days=1)
            yesterday_end = start_date
            
            yesterday_transactions = db.query(Transaction).filter(
                Transaction.business_id == business_id,
                Transaction.transaction_date >= yesterday_start,
                Transaction.transaction_date < yesterday_end
            ).all()
            
            yesterday_income = sum(t.amount for t in yesterday_transactions if t.transaction_type == 'income')
            yesterday_expenses = sum(t.amount for t in yesterday_transactions if t.transaction_type == 'expense')
            yesterday_profit = yesterday_income - yesterday_expenses
            
            # Calculate change
            if yesterday_profit > 0:
                profit_change = ((profit - yesterday_profit) / yesterday_profit) * 100
            else:
                profit_change = 0
            
            # Generate response based on language
            if language == "hi":
                content = f"Aaj ka net profit ₹{profit:,.0f} hai. Kal ₹{yesterday_profit:,.0f} tha. "
                content += f"Ye {profit_change:+.1f}% {'badh gaya' if profit_change > 0 else 'kam ho gaya'} hai."
            else:
                content = f"Today's net profit is ₹{profit:,.0f}. Yesterday it was ₹{yesterday_profit:,.0f}. "
                content += f"This is a {profit_change:+.1f}% {'increase' if profit_change > 0 else 'decrease'}."
            
            return {
                "type": "text",
                "content": content,
                "language": language,
                "data": {
                    "today_profit": profit,
                    "yesterday_profit": yesterday_profit,
                    "profit_change_percentage": round(profit_change, 2),
                    "today_income": income,
                    "today_expenses": expenses
                },
                "follow_up_actions": self.action_buttons[:2]
            }
            
        except Exception as e:
            logger.error(f"Profit response generation failed: {str(e)}")
            return {
                "type": "text",
                "content": self._get_error_message(language),
                "language": language
            }
    
    def _generate_expense_response(
        self,
        entities: Dict,
        business_id: str,
        db,
        language: str
    ) -> Dict:
        """
        Generate expense query response
        """
        
        try:
            from app.models.financial import Transaction
            from sqlalchemy import func, desc
            
            # Get top expenses this month
            end_date = datetime.utcnow()
            start_date = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            top_expenses = db.query(
                Transaction.category,
                func.sum(Transaction.amount).label('total')
            ).filter(
                Transaction.business_id == business_id,
                Transaction.transaction_type == 'expense',
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).group_by(
                Transaction.category
            ).order_by(
                desc('total')
            ).limit(5).all()
            
            # Generate response
            expenses_list = [
                {"category": cat, "amount": float(amount)}
                for cat, amount in top_expenses
            ]
            
            if language == "hi":
                content = f"Is mahine ke top expenses hain:\n"
                for i, exp in enumerate(expenses_list, 1):
                    content += f"{i}. {exp['category']}: ₹{exp['amount']:,.0f}\n"
            else:
                content = f"Here are your top expenses this month:\n"
                for i, exp in enumerate(expenses_list, 1):
                    content += f"{i}. {exp['category']}: ₹{exp['amount']:,.0f}\n"
            
            return {
                "type": "text",
                "content": content,
                "language": language,
                "data": {
                    "expenses": expenses_list
                },
                "follow_up_actions": [
                    self.action_buttons[2],
                    self.action_buttons[3]
                ]
            }
            
        except Exception as e:
            logger.error(f"Expense response generation failed: {str(e)}")
            return {
                "type": "text",
                "content": self._get_error_message(language),
                "language": language
            }
    
    def _generate_sales_response(
        self,
        entities: Dict,
        business_id: str,
        db,
        language: str
    ) -> Dict:
        """
        Generate sales query response
        """
        
        try:
            from app.models.financial import Transaction
            
            # Get sales data
            end_date = datetime.utcnow()
            start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
            
            transactions = db.query(Transaction).filter(
                Transaction.business_id == business_id,
                Transaction.transaction_type == 'income',
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).all()
            
            total_sales = sum(t.amount for t in transactions)
            sales_count = len(transactions)
            
            if language == "hi":
                content = f"Aaj ki total sales ₹{total_sales:,.0f} hai ({sales_count} transactions)."
            else:
                content = f"Today's total sales are ₹{total_sales:,.0f} ({sales_count} transactions)."
            
            return {
                "type": "text",
                "content": content,
                "language": language,
                "data": {
                    "total_sales": total_sales,
                    "sales_count": sales_count
                },
                "follow_up_actions": [
                    self.action_buttons[0],
                    self.action_buttons[2]
                ]
            }
            
        except Exception as e:
            logger.error(f"Sales response generation failed: {str(e)}")
            return {
                "type": "text",
                "content": self._get_error_message(language),
                "language": language
            }
    
    def _generate_inventory_response(
        self,
        entities: Dict,
        business_id: str,
        db,
        language: str
    ) -> Dict:
        """
        Generate inventory query response
        """
        
        try:
            from app.models.inventory import Product
            
            # Get low stock products
            products = db.query(Product).filter(
                Product.business_id == business_id,
                Product.is_active == True,
                Product.current_stock <= Product.reorder_point
            ).limit(5).all()
            
            low_stock_items = [
                {
                    "product_name": p.product_name,
                    "current_stock": p.current_stock,
                    "reorder_point": p.reorder_point
                }
                for p in products
            ]
            
            if language == "hi":
                content = f"Tamarine inventory mein {len(products)} products low stock par hain."
            else:
                content = f"You have {len(products)} products on low stock."
            
            return {
                "type": "text",
                "content": content,
                "language": language,
                "data": {
                    "low_stock_items": low_stock_items,
                    "total_low_stock": len(products)
                },
                "follow_up_actions": [
                    self.action_buttons[1],
                    self.action_buttons[3]
                ]
            }
            
        except Exception as e:
            logger.error(f"Inventory response generation failed: {str(e)}")
            return {
                "type": "text",
                "content": self._get_error_message(language),
                "language": language
            }
    
    def _generate_cash_response(
        self,
        entities: Dict,
        business_id: str,
        db,
        language: str
    ) -> Dict:
        """
        Generate cash query response
        """
        
        try:
            from app.models.financial import Transaction
            
            # Calculate cash balance
            end_date = datetime.utcnow()
            start_date = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            transactions = db.query(Transaction).filter(
                Transaction.business_id == business_id,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).all()
            
            income = sum(t.amount for t in transactions if t.transaction_type == 'income')
            expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
            cash_balance = income - expenses
            
            if language == "hi":
                content = f"Aaj ki cash balance ₹{cash_balance:,.0f} hai."
            else:
                content = f"Today's cash balance is ₹{cash_balance:,.0f}."
            
            return {
                "type": "text",
                "content": content,
                "language": language,
                "data": {
                    "cash_balance": cash_balance,
                    "monthly_income": income,
                    "monthly_expenses": expenses
                },
                "follow_up_actions": self.action_buttons
            }
            
        except Exception as e:
            logger.error(f"Cash response generation failed: {str(e)}")
            return {
                "type": "text",
                "content": self._get_error_message(language),
                "language": language
            }
    
    def _generate_health_response(
        self,
        entities: Dict,
        business_id: str,
        db,
        language: str
    ) -> Dict:
        """
        Generate financial health response
        """
        
        try:
            # In production, this would call the health scorer
            # For now, return a simplified response
            
            health_score = 78.5
            health_category = "Good"
            
            if language == "hi":
                content = f"Aapka business health score {health_score} hai jo '{health_category}' category mein aata hai. "
                content += "Aapka business achhi condition mein hai!"
            else:
                content = f"Your business health score is {health_score}, which is in the '{health_category}' category. "
                content += "Your business is in good condition!"
            
            return {
                "type": "text",
                "content": content,
                "language": language,
                "data": {
                    "health_score": health_score,
                    "health_category": health_category
                },
                "follow_up_actions": self.action_buttons
            }
            
        except Exception as e:
            logger.error(f"Health response generation failed: {str(e)}")
            return {
                "type": "text",
                "content": self._get_error_message(language),
                "language": language
            }
    
    def _generate_general_response(self, language: str) -> Dict:
        """
        Generate general response when intent is not recognized
        """
        
        if language == "hi":
            content = "Main aapki madad karne ke liye ready hoon. Aap apne sales, profit, expenses, ya inventory ke baare mein kuch bhi pooch sakte hain."
        else:
            content = "I'm here to help! You can ask me about your sales, profit, expenses, or inventory status."
        
        return {
            "type": "text",
            "content": content,
            "language": language,
            "follow_up_actions": self.action_buttons
        }
    
    def _get_error_message(self, language: str) -> str:
        """
        Get error message based on language
        """
        
        error_messages = {
            "hi": "Kripaya karein baad mein try karein. Technical error aaya hai.",
            "gu": "Kripya pachi prayas karo. Technical error aavyu che.",
            "mr": "कृपया नंतर प्रयत्न करा. Technical error आला आहे.",
            "ta": "தயவு செய்து பின்னர் முயற்சிக்கவும். Technical error ஏற்பட்டது.",
            "te": "దయచేసి తర్వాత ప్రయత్నించండి. Technical error వచ్చింది.",
            "bn": "অনুগ্রহ করে পরে চেষ্টা করুন। Technical error হয়েছে।",
            "kn": "ದಯವಿಟ್ಟು ನಂತರ ಪ್ರಯತ್ನಿಸಿ. Technical error ಆಗಿದೆ.",
            "ml": "ദയവായി പിന്നീട് ശ്രമിക്കുക. Technical error സംഭവിച്ചു.",
            "pa": "ਕਿਰਪਾ ਕਰਕੇ ਬਾਅਦ ਵਿੱਚ ਕੋਸ਼ਿਸ਼ ਕਰੋ। Technical error ਆਇਆ ਹੈ।",
            "en": "Please try again later. A technical error occurred."
        }
        
        return error_messages.get(language, error_messages["en"])