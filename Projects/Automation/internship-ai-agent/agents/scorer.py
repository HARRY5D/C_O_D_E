import logging
from typing import Dict

logger = logging.getLogger(__name__)


class OpportunityScorer:
    def __init__(self):
        self.weights = {
            'ahmedabad_location': 25,
            'startup': 20,
            'priority_role': 30,
            'internship_available': 20,
            'email_available': 5
        }
        
        self.priority_categories = ['AI/ML', 'Android', 'Mobile']
    
    def score(self, classified_data: Dict) -> Dict:
        company_name = classified_data.get('company_name', 'Unknown')
        logger.info(f"Scoring opportunity: {company_name}")
        
        score = 0
        breakdown = {}
        
        location = classified_data.get('location', '').lower()
        if 'ahmedabad' in location:
            score += self.weights['ahmedabad_location']
            breakdown['ahmedabad_location'] = self.weights['ahmedabad_location']
        
        score += self.weights['startup']
        breakdown['startup'] = self.weights['startup']
        
        category = classified_data.get('role_category', '')
        if category in self.priority_categories:
            score += self.weights['priority_role']
            breakdown['priority_role'] = self.weights['priority_role']
        
        if classified_data.get('is_internship', False):
            score += self.weights['internship_available']
            breakdown['internship_available'] = self.weights['internship_available']
        
        if classified_data.get('email', ''):
            score += self.weights['email_available']
            breakdown['email_available'] = self.weights['email_available']
        
        result = {
            'company_name': company_name,
            'role_category': category,
            'website': classified_data.get('website', ''),
            'email': classified_data.get('email', ''),
            'location': classified_data.get('location', ''),
            'score': score,
            'score_breakdown': breakdown,
            'is_internship': classified_data.get('is_internship', False),
            'career_page_url': classified_data.get('career_page_url', '')
        }
        
        logger.info(f"Scored {company_name}: {score}/100")
        
        return result
