# ========================================
# Pro-Max AFIS - Transaction Categorization Model
# ========================================
# NLP-based automatic transaction categorization
# Author: Pro-Max Development Team

from typing import Dict, List
import logging
import re

logger = logging.getLogger(__name__)


class TransactionCategorizer:
    """
    NLP-based transaction categorization using rule-based and ML approaches
    """
    
    def __init__(self):
        """Initialize the categorizer with predefined categories and rules"""
        
        # Predefined expense categories with keywords
        self.expense_categories = {
            'Inventory': ['purchase', 'stock', 'inventory', 'goods', 'product', 'material', 'raw'],
            'Rent': ['rent', 'lease', 'property', 'office space'],
            'Salaries': ['salary', 'wage', 'payroll', 'employee', 'staff', 'bonus', 'commission'],
            'Utilities': ['electricity', 'water', 'gas', 'power', 'utility', 'internet', 'phone'],
            'Marketing': ['marketing', 'advertising', 'promotion', 'campaign', 'social media', 'google ads'],
            'Travel': ['travel', 'transport', 'flight', 'train', 'taxi', 'uber', 'fuel', 'petrol', 'diesel'],
            'Office Supplies': ['office', 'stationery', 'supplies', 'furniture', 'equipment', 'printer'],
            'Insurance': ['insurance', 'coverage', 'policy'],
            'Taxes': ['tax', 'gst', 'vat', 'income tax', 'tds', 'professional tax'],
            'Banking': ['bank', 'charge', 'fee', 'interest', 'loan'],
            'Software': ['software', 'subscription', 'saas', 'app', 'tool', 'platform'],
            'Repairs & Maintenance': ['repair', 'maintenance', 'service', 'fix'],
            'Professional Services': ['consultant', 'legal', 'accounting', 'audit', 'advisory'],
            'Training': ['training', 'education', 'course', 'workshop', 'seminar'],
            'Entertainment': ['entertainment', 'dining', 'restaurant', 'food', 'lunch', 'dinner']
        }
        
        # Predefined income categories with keywords
        self.income_categories = {
            'Sales': ['sale', 'sold', 'revenue', 'income', 'invoice', 'billing'],
            'Services': ['service', 'consulting', 'professional fees', 'hourly'],
            'Interest': ['interest', 'dividend'],
            'Refunds': ['refund', 'return', 'reimbursement'],
            'Other Income': ['other', 'miscellaneous', 'bonus', 'commission']
        }
        
        # Subcategory mappings
        self.subcategories = {
            'Inventory': ['Raw Materials', 'Finished Goods', 'Packaging', 'Components'],
            'Sales': ['Product Sales', 'Online Sales', 'Retail Sales', 'Wholesale'],
            'Utilities': ['Electricity', 'Internet', 'Water', 'Gas'],
            'Marketing': ['Digital Marketing', 'Print Ads', 'Events', 'Social Media']
        }
        
        # Suggested tags for categories
        self.suggested_tags = {
            'Inventory': ['reorder', 'stock', 'purchase'],
            'Sales': ['revenue', 'customer', 'order'],
            'Marketing': ['promotion', 'campaign', 'advertising']
        }
        
        logger.info("TransactionCategorizer initialized")
    
    def categorize(
        self,
        description: str,
        transaction_type: str = "expense"
    ) -> Dict:
        """
        Categorize a transaction based on description
        
        Args:
            description: Transaction description text
            transaction_type: Type of transaction ('income' or 'expense')
            
        Returns:
            Dictionary containing category, subcategory, confidence, and suggested tags
        """
        
        try:
            # Clean and normalize description
            cleaned_description = self._clean_description(description)
            
            # Get appropriate category dictionary
            categories = self.expense_categories if transaction_type == "expense" else self.income_categories
            
            # Calculate category scores
            category_scores = self._calculate_category_scores(cleaned_description, categories)
            
            # Get best category
            if category_scores:
                best_category, best_score = max(category_scores.items(), key=lambda x: x[1])
            else:
                best_category = "Uncategorized"
                best_score = 0
            
            # Get subcategory
            subcategory = self._get_subcategory(best_category, cleaned_description)
            
            # Get suggested tags
            suggested_tags = self._get_suggested_tags(best_category)
            
            # Calculate confidence
            confidence = min(1.0, best_score / 5.0) if best_score > 0 else 0.0
            
            return {
                'category': best_category,
                'subcategory': subcategory,
                'confidence': round(confidence, 2),
                'suggested_tags': suggested_tags,
                'method': 'rule_based'
            }
            
        except Exception as e:
            logger.error(f"Categorization failed: {str(e)}")
            return {
                'category': 'Uncategorized',
                'subcategory': None,
                'confidence': 0.0,
                'suggested_tags': [],
                'method': 'rule_based'
            }
    
    def _clean_description(self, description: str) -> str:
        """
        Clean and normalize transaction description
        
        Args:
            description: Raw description text
            
        Returns:
            Cleaned description
        """
        
        # Convert to lowercase
        cleaned = description.lower()
        
        # Remove special characters
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', cleaned)
        
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        
        return cleaned
    
    def _calculate_category_scores(
        self,
        description: str,
        categories: Dict[str, List[str]]
    ) -> Dict[str, float]:
        """
        Calculate category scores based on keyword matching
        
        Args:
            description: Cleaned description text
            categories: Dictionary of categories and their keywords
            
        Returns:
            Dictionary of categories with their scores
        """
        
        scores = {}
        description_words = set(description.split())
        
        for category, keywords in categories.items():
            score = 0
            matched_keywords = []
            
            for keyword in keywords:
                keyword_words = keyword.split()
                # Check if all words in keyword are present
                if all(word in description for word in keyword_words):
                    score += 1
                    matched_keywords.append(keyword)
                # Also check individual words
                elif len(keyword_words) == 1 and keyword in description_words:
                    score += 0.5
                    matched_keywords.append(keyword)
            
            if score > 0:
                scores[category] = score
        
        return scores
    
    def _get_subcategory(
        self,
        category: str,
        description: str
    ) -> str:
        """
        Get subcategory based on category and description
        
        Args:
            category: Main category
            description: Transaction description
            
        Returns:
            Subcategory string or None
        """
        
        if category not in self.subcategories:
            return None
        
        subcategories = self.subcategories[category]
        
        # Simple matching - in production, use more sophisticated NLP
        for subcategory in subcategories:
            sub_keywords = subcategory.lower().split()
            if any(keyword in description for keyword in sub_keywords):
                return subcategory
        
        return None
    
    def _get_suggested_tags(self, category: str) -> List[str]:
        """
        Get suggested tags for a category
        
        Args:
            category: Main category
            
        Returns:
            List of suggested tags
        """
        
        return self.suggested_tags.get(category, [])