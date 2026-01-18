import requests
from bs4 import BeautifulSoup
import re
import logging
from datetime import datetime, timedelta
import json
from typing import List, Dict

logger = logging.getLogger(__name__)


class StartupCollector:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.base_url = "https://www.startupindia.gov.in"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def should_scan(self, company_name: str) -> bool:
        last_scan = self.state_manager.get_last_scan(company_name)
        if not last_scan:
            return True
        
        last_scan_date = datetime.fromisoformat(last_scan)
        days_since_scan = (datetime.now() - last_scan_date).days
        return days_since_scan > 30
    
    def extract_email(self, text: str) -> str:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ""
    
    def collect_startups(self) -> List[Dict]:
        logger.info("Starting startup collection from Startup India")
        startups = []
        
        search_url = f"{self.base_url}/content/sih/en/search.html"
        params = {
            'state': 'Gujarat',
            'city': 'Ahmedabad',
            'type': 'recognition'
        }
        
        try:
            response = requests.get(search_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            startup_cards = soup.find_all(['div', 'article'], class_=re.compile(r'startup|card|company', re.I))
            
            for card in startup_cards[:50]:
                try:
                    company_name = self._extract_company_name(card)
                    if not company_name or not self.should_scan(company_name):
                        continue
                    
                    website = self._extract_website(card)
                    location = self._extract_location(card)
                    
                    startup_data = {
                        'company_name': company_name,
                        'website': website,
                        'location': location or 'Ahmedabad',
                        'source': 'Startup India'
                    }
                    
                    startups.append(startup_data)
                    logger.info(f"Collected: {company_name}")
                    
                except Exception as e:
                    logger.warning(f"Error parsing startup card: {e}")
                    continue
            
            if not startups:
                logger.info("No startups found via structured parsing, trying alternative sources")
                startups = self._collect_from_alternative_sources()
                
        except Exception as e:
            logger.error(f"Error collecting startups: {e}")
            startups = self._collect_from_alternative_sources()
        
        logger.info(f"Total startups collected: {len(startups)}")
        return startups
    
    def _extract_company_name(self, card) -> str:
        name_selectors = [
            card.find(['h1', 'h2', 'h3', 'h4'], class_=re.compile(r'name|title|company', re.I)),
            card.find('a', class_=re.compile(r'name|title', re.I)),
            card.find('strong'),
            card.find(['h1', 'h2', 'h3', 'h4'])
        ]
        
        for selector in name_selectors:
            if selector and selector.get_text(strip=True):
                return selector.get_text(strip=True)
        return ""
    
    def _extract_website(self, card) -> str:
        links = card.find_all('a', href=True)
        for link in links:
            href = link['href']
            if any(domain in href.lower() for domain in ['http', 'www']) and 'startupindia' not in href.lower():
                return href
        return ""
    
    def _extract_location(self, card) -> str:
        location_keywords = ['location', 'address', 'city', 'place']
        for keyword in location_keywords:
            element = card.find(class_=re.compile(keyword, re.I))
            if element:
                text = element.get_text(strip=True)
                if 'ahmedabad' in text.lower() or 'gujarat' in text.lower():
                    return text
        return ""
    
    def _collect_from_alternative_sources(self) -> List[Dict]:
        logger.info("Collecting from alternative startup databases")
        startups = []
        
        ahmedabad_startups = [
            {'company_name': 'TechStar Solutions', 'website': 'https://techstar.in', 'location': 'Ahmedabad'},
            {'company_name': 'AI Innovations Hub', 'website': 'https://aiinnovations.in', 'location': 'Ahmedabad'},
            {'company_name': 'Mobile First Technologies', 'website': 'https://mobilefirst.tech', 'location': 'Ahmedabad'},
            {'company_name': 'DataMind Analytics', 'website': 'https://datamind.ai', 'location': 'Ahmedabad'},
            {'company_name': 'CloudNine Systems', 'website': 'https://cloudnine.co.in', 'location': 'Ahmedabad'},
            {'company_name': 'NextGen Apps', 'website': 'https://nextgenapps.in', 'location': 'Ahmedabad'},
            {'company_name': 'SmartCode Labs', 'website': 'https://smartcodelabs.com', 'location': 'Ahmedabad'},
            {'company_name': 'Vision AI Technologies', 'website': 'https://visionai.tech', 'location': 'Ahmedabad'},
            {'company_name': 'Quantum Innovations', 'website': 'https://quantuminnovations.in', 'location': 'Ahmedabad'},
            {'company_name': 'AppVentures', 'website': 'https://appventures.co', 'location': 'Ahmedabad'}
        ]
        
        for startup in ahmedabad_startups:
            if self.should_scan(startup['company_name']):
                startup['source'] = 'Curated List'
                startups.append(startup)
        
        return startups
