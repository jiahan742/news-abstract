"""
摘要生成模块

Responsible for:
- Generating structured summaries
- Extracting key information (characters, time, event, result)
- Using NLP techniques for analysis
"""

import logging
from typing import Dict, Optional, List
from datetime import datetime
from src.news_fetcher import NewsFetcher
from src.language_detector import LanguageDetector
from src.content_extractor import ContentExtractor
from src.summary_formatter import SummaryFormatter

logger = logging.getLogger(__name__)


class NewsAbstractGenerator:
    """
    Main class for generating news abstracts with structured information:
    - Characters (Who)
    - Time (When)
    - Event (What)
    - Result (Outcome)
    """

    def __init__(self):
        self.fetcher = NewsFetcher()
        self.language_detector = LanguageDetector()
        self.content_extractor = ContentExtractor()
        self.formatter = SummaryFormatter()
        logger.info("NewsAbstractGenerator initialized")

    def extract_characters(self, text: str) -> List[str]:
        """
        Extract named entities (persons, organizations) from text
        
        Args:
            text: Input text
            
        Returns:
            List of identified characters/organizations
        """
        # Placeholder: would use spaCy or transformers for NER
        # This is a simple implementation
        characters = []
        
        # Simple pattern: capitalize words that might be names
        words = text.split()
        for i, word in enumerate(words):
            if word[0].isupper() and len(word) > 2:
                # Check if followed by surname or title
                if i + 1 < len(words) and words[i+1][0].isupper():
                    characters.append(f"{word} {words[i+1]}")
        
        return list(set(characters))[:10]  # Return top 10 unique

    def extract_time(self, text: str) -> Optional[str]:
        """
        Extract temporal information from text
        
        Args:
            text: Input text
            
        Returns:
            Extracted time information
        """
        # Placeholder: would use more sophisticated time extraction
        # Look for common date patterns
        import re
        
        # Pattern for dates like "May 7, 2026" or "2026-05-07"
        date_patterns = [
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
            r'\d{4}-\d{2}-\d{2}',
            r'\d{1,2}/\d{1,2}/\d{4}',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        # Fallback to current date
        return datetime.now().strftime('%B %d, %Y')

    def extract_event(self, text: str, max_length: int = 300) -> str:
        """
        Extract the main event description
        
        Args:
            text: Input text
            max_length: Maximum length for event description
            
        Returns:
            Event description
        """
        # Get key sentences
        sentences = self.content_extractor.extract_key_sentences(text, top_n=3)
        
        if sentences:
            event = ' '.join(sentences)
            return event[:max_length] if len(event) > max_length else event
        
        # Fallback to first paragraph
        paragraphs = self.content_extractor.extract_paragraphs(text)
        if paragraphs:
            return paragraphs[0][:max_length]
        
        return text[:max_length]

    def extract_result(self, text: str, max_length: int = 200) -> str:
        """
        Extract the result or consequence of the event
        
        Args:
            text: Input text
            max_length: Maximum length for result
            
        Returns:
            Result/consequence description
        """
        # Look for result-indicating words
        result_keywords = ['result', 'outcome', 'consequence', 'impact', 'effect', 'lead to', 'caused']
        
        paragraphs = self.content_extractor.extract_paragraphs(text)
        
        # Find paragraphs with result keywords
        for para in paragraphs[-3:]:  # Check last 3 paragraphs
            para_lower = para.lower()
            if any(keyword in para_lower for keyword in result_keywords):
                return para[:max_length]
        
        # Fallback to last paragraph
        if paragraphs:
            return paragraphs[-1][:max_length]
        
        return "Ongoing situation being monitored."

    def process_url(self, url: str) -> Optional[Dict]:
        """
        Process a news URL and generate structured summary
        
        Args:
            url: News article URL
            
        Returns:
            Dictionary with structured summary or None if processing failed
        """
        logger.info(f"Processing URL: {url}")
        
        # Fetch content
        result = self.fetcher.process_url(url)
        if not result:
            logger.error(f"Failed to fetch content from {url}")
            return None
        
        content = result['content']
        metadata = result['metadata']
        
        # Detect language
        lang_result = self.language_detector.detect_language(content)
        if not lang_result:
            lang_code = 'unknown'
            confidence = 0
        else:
            lang_code, confidence = lang_result
        
        # Extract main content
        main_content = self.content_extractor.extract_main_content(content)
        if not main_content:
            logger.error("Failed to extract main content")
            return None
        
        # Extract structured information
        characters = self.extract_characters(main_content)
        time_info = self.extract_time(main_content)
        event = self.extract_event(main_content)
        result = self.extract_result(main_content)
        
        # Create summary
        summary = {
            'title': metadata.get('title', 'Untitled'),
            'url': url,
            'original_language': lang_code,
            'language_confidence': confidence,
            'publish_date': metadata.get('publish_date'),
            'summary': {
                'characters': characters,
                'time': time_info,
                'event': event,
                'result': result
            },
            'processed_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        logger.info(f"Successfully generated summary for: {url}")
        return summary

    def process_text(self, text: str, title: str = "News") -> Optional[Dict]:
        """
        Process raw text and generate summary
        
        Args:
            text: Raw news text
            title: Article title
            
        Returns:
            Dictionary with structured summary
        """
        logger.info("Processing raw text")
        
        # Detect language
        lang_result = self.language_detector.detect_language(text)
        if not lang_result:
            lang_code = 'unknown'
            confidence = 0
        else:
            lang_code, confidence = lang_result
        
        # Extract main content
        main_content = self.content_extractor.extract_main_content(text)
        if not main_content:
            return None
        
        # Extract structured information
        characters = self.extract_characters(main_content)
        time_info = self.extract_time(main_content)
        event = self.extract_event(main_content)
        result = self.extract_result(main_content)
        
        # Create summary
        summary = {
            'title': title,
            'original_language': lang_code,
            'language_confidence': confidence,
            'summary': {
                'characters': characters,
                'time': time_info,
                'event': event,
                'result': result
            },
            'processed_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        return summary
