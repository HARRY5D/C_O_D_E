import re
from typing import List


class EmailRanker:
    def __init__(self):
        self.priority_domains = [
            'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com'
        ]
        
        self.role_keywords = {
            'hr': 10,
            'career': 9,
            'jobs': 9,
            'recruitment': 8,
            'hiring': 8,
            'talent': 7,
            'intern': 9,
            'contact': 5,
            'info': 3
        }
    
    def rank_emails(self, emails: List[str]) -> str:
        if not emails:
            return ""
        
        if len(emails) == 1:
            return emails[0]
        
        scored_emails = []
        for email in emails:
            score = self._score_email(email)
            scored_emails.append((email, score))
        
        scored_emails.sort(key=lambda x: x[1], reverse=True)
        return scored_emails[0][0]
    
    def _score_email(self, email: str) -> int:
        score = 0
        email_lower = email.lower()
        
        local_part = email_lower.split('@')[0]
        
        for keyword, points in self.role_keywords.items():
            if keyword in local_part:
                score += points
        
        domain = email_lower.split('@')[1] if '@' in email_lower else ''
        if domain not in self.priority_domains:
            score += 5
        
        return score
    
    def is_valid_email(self, email: str) -> bool:
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        if not re.match(pattern, email):
            return False
        
        invalid_patterns = [
            'noreply', 'no-reply', 'donotreply', 
            'example.com', 'test.com', 'domain.com'
        ]
        
        return not any(pattern in email.lower() for pattern in invalid_patterns)
