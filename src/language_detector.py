"""
语言检测模块

Responsible for:
- Detecting the language of text
- Supporting multiple languages
- Providing language information
"""

import logging
from typing import Optional, Tuple
from langdetect import detect, detect_langs, LangDetectException
from config import SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

# Language code to name mapping
LANGUAGE_NAMES = {
    'en': 'English',
    'zh': 'Chinese',
    'zh-cn': 'Simplified Chinese',
    'zh-tw': 'Traditional Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'ru': 'Russian',
    'pt': 'Portuguese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'it': 'Italian',
    'nl': 'Dutch',
    'tr': 'Turkish',
    'vi': 'Vietnamese',
    'id': 'Indonesian',
    'th': 'Thai',
    'pl': 'Polish',
    'uk': 'Ukrainian',
    'cs': 'Czech'
}


class LanguageDetector:
    """
    Detects the language of given text
    """

    def __init__(self):
        self.supported_languages = SUPPORTED_LANGUAGES
        logger.info(f"LanguageDetector initialized with {len(self.supported_languages)} supported languages")

    def detect_language(self, text: str) -> Optional[Tuple[str, float]]:
        """
        Detect the primary language of text
        
        Args:
            text: Input text to detect
            
        Returns:
            Tuple of (language_code, confidence) or None if detection failed
        """
        if not text or len(text.strip()) < 10:
            logger.warning("Text too short for reliable detection")
            return None
        
        try:
            # Detect all possible languages with probabilities
            results = detect_langs(text)
            
            if results:
                primary = results[0]  # Highest probability
                lang_code = primary.lang
                confidence = primary.prob
                
                logger.debug(f"Detected language: {lang_code} (confidence: {confidence:.2%})")
                return lang_code, confidence
            
        except LangDetectException as e:
            logger.error(f"Language detection failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in language detection: {e}")
        
        return None

    def detect_multiple_languages(self, text: str) -> Optional[list]:
        """
        Detect multiple possible languages with confidence scores
        
        Args:
            text: Input text to detect
            
        Returns:
            List of (language_code, confidence) tuples sorted by confidence
        """
        if not text or len(text.strip()) < 10:
            return None
        
        try:
            results = detect_langs(text)
            return [(r.lang, r.prob) for r in results]
        except Exception as e:
            logger.error(f"Error detecting multiple languages: {e}")
            return None

    def get_language_name(self, lang_code: str) -> str:
        """
        Get human-readable language name from code
        
        Args:
            lang_code: Language code (e.g., 'en', 'zh')
            
        Returns:
            Language name or original code if not found
        """
        return LANGUAGE_NAMES.get(lang_code.lower(), lang_code)

    def is_supported_language(self, lang_code: str) -> bool:
        """
        Check if language is in supported list
        
        Args:
            lang_code: Language code
            
        Returns:
            True if supported, False otherwise
        """
        return lang_code in self.supported_languages
