import requests
from bs4 import BeautifulSoup
import re
import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)


class CareerPageCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.career_patterns = [
            r'career', r'jobs', r'internship', r'opportunities', 
            r'work-with-us', r'join-us', r'hiring', r'openings',
            r'intern', r'recruitment', r'vacancy', r'position'
        ]
        self.timeout = 15
    
    def crawl_startup(self, startup_data: Dict) -> Dict:
        website = startup_data.get('website', '')
        company_name = startup_data.get('company_name', 'Unknown')
        
        logger.info(f"Crawling: {company_name}")
        
        result = {
            'company_name': company_name,
            'website': website,
            'location': startup_data.get('location', ''),
            'career_page_url': '',
            'career_page_text': '',
            'email': '',
            'has_internship': False
        }
        
        if not website:
            logger.warning(f"No website for {company_name}")
            return result
        
        try:
            homepage_content = self._fetch_page(website)
            if not homepage_content:
                return result
            
            career_url = self._find_career_page(website, homepage_content)
            
            if career_url:
                result['career_page_url'] = career_url
                career_content = self._fetch_page(career_url)
                if career_content:
                    result['career_page_text'] = self._extract_text(career_content)
                    result['email'] = self._extract_email(career_content)
                    result['has_internship'] = self._detect_internship(result['career_page_text'])
            else:
                result['career_page_text'] = self._extract_text(homepage_content)
                result['email'] = self._extract_email(homepage_content)
                result['has_internship'] = self._detect_internship(result['career_page_text'])
            
            logger.info(f"Crawled {company_name}: Career page={'found' if career_url else 'not found'}, Email={'found' if result['email'] else 'not found'}")
            
        except Exception as e:
            logger.error(f"Error crawling {company_name}: {e}")
        
        return result
    
    def _fetch_page(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return None
    
    def _find_career_page(self, base_url: str, homepage_html: str) -> Optional[str]:
        soup = BeautifulSoup(homepage_html, 'html.parser')
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            link_text = link.get_text(strip=True).lower()
            
            for pattern in self.career_patterns:
                if re.search(pattern, href.lower()) or re.search(pattern, link_text):
                    full_url = urljoin(base_url, href)
                    if self._is_valid_url(full_url):
                        return full_url
        
        return None
    
    def _is_valid_url(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
            return bool(parsed.scheme and parsed.netloc)
        except:
            return False
    
    def _extract_text(self, html: str) -> str:
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            for script in soup(["script", "style", "meta", "link"]):
                script.decompose()
            
            text = soup.get_text(separator=' ', strip=True)
            text = re.sub(r'\s+', ' ', text)
            
            return text[:10000]
        except Exception as e:
            logger.warning(f"Error extracting text: {e}")
            return ""
    
    def _extract_email(self, html: str) -> str:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html)
        
        valid_emails = [email for email in emails if not any(
            skip in email.lower() for skip in ['example.com', 'test.com', 'domain.com', 'yourcompany.com']
        )]
        
        return valid_emails[0] if valid_emails else ""
    
    def _detect_internship(self, text: str) -> bool:
        internship_keywords = [
            'internship', 'intern position', 'summer intern', 
            'winter intern', 'intern opening', 'trainee'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in internship_keywords)
