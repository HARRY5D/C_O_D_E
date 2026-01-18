import re
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


class RoleClassifier:
    def __init__(self):
        self.categories = {
            'AI/ML': [
                'machine learning', 'deep learning', 'artificial intelligence',
                'neural network', 'tensorflow', 'pytorch', 'keras',
                'computer vision', 'nlp', 'natural language processing',
                'data science', 'ml engineer', 'ai engineer', 'ml model',
                'predictive model', 'reinforcement learning', 'llm', 'gpt'
            ],
            'Android': [
                'android', 'kotlin', 'android studio', 'android developer',
                'mobile app android', 'android sdk', 'android application',
                'java android', 'jetpack compose', 'android framework'
            ],
            'Mobile': [
                'mobile', 'flutter', 'react native', 'ios', 'swift',
                'mobile developer', 'mobile app', 'cross platform',
                'xamarin', 'mobile development', 'app development',
                'smartphone', 'mobile application'
            ],
            'Web': [
                'web developer', 'frontend', 'backend', 'full stack',
                'react', 'angular', 'vue', 'node.js', 'django', 'flask',
                'javascript', 'html', 'css', 'web development', 'rest api',
                'web application', 'responsive design'
            ],
            'Other': []
        }
        
        self.internship_keywords = [
            'internship', 'intern', 'trainee', 'summer internship',
            'winter internship', 'intern position', 'intern opening',
            'internship opportunity', 'student internship'
        ]
    
    def classify(self, crawled_data: Dict) -> Dict:
        text = crawled_data.get('career_page_text', '')
        company_name = crawled_data.get('company_name', 'Unknown')
        
        logger.info(f"Classifying roles for: {company_name}")
        
        category, confidence = self._categorize_role(text)
        is_internship = self._is_internship_available(text, crawled_data)
        
        result = {
            'company_name': company_name,
            'website': crawled_data.get('website', ''),
            'location': crawled_data.get('location', ''),
            'email': crawled_data.get('email', ''),
            'role_category': category,
            'confidence': confidence,
            'is_internship': is_internship,
            'career_page_url': crawled_data.get('career_page_url', '')
        }
        
        logger.info(f"Classified {company_name}: {category} (confidence: {confidence:.2f}), Internship: {is_internship}")
        
        return result
    
    def _categorize_role(self, text: str) -> Tuple[str, float]:
        if not text:
            return 'Other', 0.0
        
        text_lower = text.lower()
        scores = {}
        
        for category, keywords in self.categories.items():
            if category == 'Other':
                continue
            
            score = 0
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, text_lower))
                score += matches
            
            scores[category] = score
        
        if not any(scores.values()):
            return 'Other', 0.0
        
        max_category = max(scores.items(), key=lambda x: x[1])
        category, raw_score = max_category
        
        total_keywords = len(self.categories[category])
        confidence = min(raw_score / total_keywords, 1.0)
        
        return category, round(confidence, 2)
    
    def _is_internship_available(self, text: str, crawled_data: Dict) -> bool:
        has_internship_flag = crawled_data.get('has_internship', False)
        if has_internship_flag:
            return True
        
        if not text:
            return False
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.internship_keywords)
