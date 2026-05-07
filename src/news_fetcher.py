"""
新闻网页爬取模块

Responsible for:
- Fetching web content from URLs
- Handling different encodings
- Extracting news metadata
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse
from config import REQUEST_TIMEOUT, USER_AGENT, MAX_RETRIES

logger = logging.getLogger(__name__)


class NewsFetcher:
    """
    Fetches news content from web URLs
    """

    def __init__(self):
        self.timeout = REQUEST_TIMEOUT
        self.user_agent = USER_AGENT
        self.max_retries = MAX_RETRIES
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})

    def fetch_content(self, url: str) -> Optional[Tuple[str, str]]:
        """
        Fetch raw HTML content from URL
        
        Args:
            url: Target URL
            
        Returns:
            Tuple of (html_content, detected_encoding) or None if failed
        """
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                # Detect encoding
                encoding = response.encoding or 'utf-8'
                html_content = response.content.decode(encoding, errors='ignore')
                
                logger.info(f"Successfully fetched: {url}")
                return html_content, encoding
                
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed: {e}")
                if attempt == self.max_retries - 1:
                    logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
                    return None

    def extract_text(self, html_content: str) -> Optional[str]:
        """
        Extract main text content from HTML
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            Extracted text content or None
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style']):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator=' ', strip=True)
            return text if text else None
            
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return None

    def extract_metadata(self, html_content: str, url: str) -> Dict:
        """
        Extract metadata from HTML (title, description, etc.)
        
        Args:
            html_content: Raw HTML content
            url: Source URL
            
        Returns:
            Dictionary with metadata
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            metadata = {
                'url': url,
                'title': soup.title.string if soup.title else None,
                'description': None,
                'image': None,
                'publish_date': None
            }
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                metadata['description'] = meta_desc.get('content')
            
            # Extract og:image
            og_image = soup.find('meta', attrs={'property': 'og:image'})
            if og_image:
                metadata['image'] = og_image.get('content')
            
            # Extract publish date
            pub_date = soup.find('meta', attrs={'property': 'article:published_time'})
            if pub_date:
                metadata['publish_date'] = pub_date.get('content')
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            return {'url': url}

    def process_url(self, url: str) -> Optional[Dict]:
        """
        Process a URL and return extracted content and metadata
        
        Args:
            url: Target URL
            
        Returns:
            Dictionary with 'content' and 'metadata' keys or None
        """
        result = self.fetch_content(url)
        if not result:
            return None
        
        html_content, encoding = result
        text_content = self.extract_text(html_content)
        metadata = self.extract_metadata(html_content, url)
        
        if not text_content:
            logger.warning(f"No text content extracted from {url}")
            return None
        
        return {
            'content': text_content,
            'metadata': metadata,
            'encoding': encoding
        }
