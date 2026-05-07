"""
配置文件 - 新闻摘要助手
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 基础配置
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# 网页爬取配置
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '10'))
USER_AGENT = os.getenv(
    'USER_AGENT',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
)
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))

# 语言检测配置
SUPPORTED_LANGUAGES = [
    'en', 'zh', 'ja', 'ko', 'es', 'fr', 'de', 'ru', 'pt', 'ar',
    'hi', 'it', 'nl', 'tr', 'vi', 'id', 'th', 'pl', 'uk', 'cs'
]

# NLP 模型配置
NLP_MODEL = os.getenv('NLP_MODEL', 'spacy')
TRANSFORMER_MODEL = os.getenv(
    'TRANSFORMER_MODEL',
    'bert-base-multilingual-cased'
)

# 摘要配置
SUMMARY_MIN_LENGTH = int(os.getenv('SUMMARY_MIN_LENGTH', '50'))
SUMMARY_MAX_LENGTH = int(os.getenv('SUMMARY_MAX_LENGTH', '500'))
EXTRACT_ENTITIES = os.getenv('EXTRACT_ENTITIES', 'True').lower() == 'true'

# 缓存配置
USE_CACHE = os.getenv('USE_CACHE', 'True').lower() == 'true'
CACHE_DIR = os.getenv('CACHE_DIR', './cache')
CACHE_EXPIRY = int(os.getenv('CACHE_EXPIRY', '86400'))  # 24小时

# 输出格式
OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'json')  # json, markdown, text

if __name__ == '__main__':
    print("配置已加载")
