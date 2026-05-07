"""
内容提取模块

Responsible for:
- Extracting main news content from text
- Removing noise and irrelevant information
- Preserving document structure
"""

import logging
from typing import Dict, Optional
import re
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ContentExtractor:
    """
    Extracts main content from news articles
    """

    def __init__(self):
        self.min_content_length = 100  # Minimum characters for valid content
        
        # Common unwanted text patterns
        self.noise_patterns = [
            r'(\n\s*){3,}',  # Multiple empty lines
            r'\s{2,}(?=\w)',  # Multiple spaces
            r'Copyright.*?\d{4}',  # Copyright notices
            r'Share this.*?email',  # Share buttons
        ]

    def extract_paragraphs(self, text: str) -> list:
        """
        Extract and clean paragraphs from text
        
        Args:
            text: Raw text content
            
        Returns:
            List of cleaned paragraphs
        """
        if not text:
            return []
        
        # Split by multiple newlines
        paragraphs = text.split('\n\n')
        
        # Clean and filter paragraphs
        cleaned = []
        for para in paragraphs:
            cleaned_para = para.strip()
            # Only keep paragraphs with reasonable length
            if len(cleaned_para) >= 20:  # At least 20 characters
                cleaned.append(cleaned_para)
        
        return cleaned

    def remove_noise(self, text: str) -> str:
        """
        Remove noise from text
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        cleaned = text
        
        # Apply noise removal patterns
        for pattern in self.noise_patterns:
            cleaned = re.sub(pattern, '\n', cleaned, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove common boilerplate
        cleaned = re.sub(r'(?i)(advertisement|ad|sponsored content).*?\n', '\n', cleaned)
        
        return cleaned.strip()

    def extract_sentences(self, text: str) -> list:
        """
        Extract sentences from text
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting (can be improved with NLTK)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        # Filter empty sentences
        return [s.strip() for s in sentences if len(s.strip()) > 10]

    def extract_main_content(self, text: str) -> Optional[str]:
        """
        Extract main news content
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned main content or None
        """
        if not text or len(text) < self.min_content_length:
            logger.warning("Content too short for extraction")
            return None
        
        # Remove noise
        cleaned = self.remove_noise(text)
        
        # Extract paragraphs
        paragraphs = self.extract_paragraphs(cleaned)
        
        if not paragraphs:
            logger.warning("No valid paragraphs extracted")
            return None
        
        # Combine paragraphs with newlines
        main_content = '\n\n'.join(paragraphs)
        
        logger.debug(f"Extracted {len(paragraphs)} paragraphs, total length: {len(main_content)}")
        return main_content

    def extract_key_sentences(self, text: str, top_n: int = 5) -> list:
        """
        Extract top N key sentences from content
        
        Args:
            text: Input text
            top_n: Number of key sentences to extract
            
        Returns:
            List of key sentences
        """
        sentences = self.extract_sentences(text)
        
        if not sentences:
            return []
        
        # Simple heuristic: longer sentences tend to contain more information
        # Better approach would use TF-IDF or similar
        sorted_sentences = sorted(
            enumerate(sentences),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        # Return top N in original order
        key_indices = sorted([idx for idx, _ in sorted_sentences[:top_n]])
        return [sentences[i] for i in key_indices]
