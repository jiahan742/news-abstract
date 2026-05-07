"""
测试模块 - 新闻摘要助手
"""

import pytest
from src.language_detector import LanguageDetector
from src.content_extractor import ContentExtractor
from src.abstract_generator import NewsAbstractGenerator


class TestLanguageDetector:
    """Test language detection functionality"""
    
    def setup_method(self):
        self.detector = LanguageDetector()
    
    def test_detect_english(self):
        text = "This is an English news article about recent events."
        lang, confidence = self.detector.detect_language(text)
        assert lang == 'en'
        assert confidence > 0.5
    
    def test_detect_chinese(self):
        text = "这是一篇关于最近事件的中文新闻文章。"
        lang, confidence = self.detector.detect_language(text)
        assert lang == 'zh'
        assert confidence > 0.5
    
    def test_detect_spanish(self):
        text = "Este es un artículo de noticias en español sobre eventos recientes."
        lang, confidence = self.detector.detect_language(text)
        assert lang == 'es'
        assert confidence > 0.5
    
    def test_short_text(self):
        text = "Hi"
        result = self.detector.detect_language(text)
        assert result is None


class TestContentExtractor:
    """Test content extraction functionality"""
    
    def setup_method(self):
        self.extractor = ContentExtractor()
    
    def test_extract_paragraphs(self):
        text = "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3."
        paragraphs = self.extractor.extract_paragraphs(text)
        assert len(paragraphs) == 3
    
    def test_remove_noise(self):
        text = "Important content.\n\n\nAdvertisement stuff.   Extra spaces."
        cleaned = self.extractor.remove_noise(text)
        assert len(cleaned) > 0
        assert "Important" in cleaned
    
    def test_extract_sentences(self):
        text = "This is first sentence. This is second sentence! This is third sentence?"
        sentences = self.extractor.extract_sentences(text)
        assert len(sentences) >= 2


class TestNewsAbstractGenerator:
    """Test news abstract generation functionality"""
    
    def setup_method(self):
        self.generator = NewsAbstractGenerator()
    
    def test_extract_time(self):
        text = "On May 7, 2026, the government announced new policies."
        time_info = self.generator.extract_time(text)
        assert time_info is not None
        assert "May" in time_info or "2026" in time_info
    
    def test_extract_characters(self):
        text = "President John Smith and Minister Jane Doe announced new policies today."
        characters = self.generator.extract_characters(text)
        assert len(characters) > 0
    
    def test_extract_event(self):
        text = "The government announced new environmental policies today. These policies will affect millions."
        event = self.generator.extract_event(text)
        assert len(event) > 0
        assert "government" in event.lower() or "policies" in event.lower()
    
    def test_extract_result(self):
        text = "The company released new software. As a result, sales increased by 30%."
        result = self.generator.extract_result(text)
        assert len(result) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
