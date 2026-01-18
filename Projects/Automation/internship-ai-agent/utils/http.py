import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class HTTPClient:
    def __init__(self, timeout: int = 15, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def get(self, url: str, custom_headers: Optional[dict] = None) -> Optional[requests.Response]:
        headers = self.headers.copy()
        if custom_headers:
            headers.update(custom_headers)
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    allow_redirects=True,
                    verify=True
                )
                
                if response.status_code == 200:
                    return response
                elif response.status_code in [301, 302, 303, 307, 308]:
                    continue
                elif response.status_code == 403:
                    logger.warning(f"Access forbidden for {url}")
                    return None
                elif response.status_code == 404:
                    logger.warning(f"Page not found: {url}")
                    return None
                else:
                    logger.warning(f"HTTP {response.status_code} for {url}")
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1} for {url}")
            except requests.exceptions.SSLError:
                logger.warning(f"SSL error for {url}")
                return None
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error for {url}")
            except Exception as e:
                logger.error(f"Unexpected error fetching {url}: {e}")
                
        return None
    
    def post(self, url: str, data: dict, custom_headers: Optional[dict] = None) -> Optional[requests.Response]:
        headers = self.headers.copy()
        if custom_headers:
            headers.update(custom_headers)
        
        try:
            response = requests.post(
                url,
                data=data,
                headers=headers,
                timeout=self.timeout,
                allow_redirects=True,
                verify=True
            )
            
            return response if response.status_code == 200 else None
            
        except Exception as e:
            logger.error(f"POST request failed for {url}: {e}")
            return None
