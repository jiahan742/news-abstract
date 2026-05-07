"""
主程序入口 - 新闻摘要助手
"""

import logging
import sys
from src.abstract_generator import NewsAbstractGenerator
from config import DEBUG, LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for the news abstract assistant
    """
    logger.info("Starting News Abstract Assistant")
    
    try:
        # Initialize generator
        generator = NewsAbstractGenerator()
        
        # Example usage
        if len(sys.argv) > 1:
            url = sys.argv[1]
            logger.info(f"Processing URL: {url}")
            
            summary = generator.process_url(url)
            
            if summary:
                # Format and print summary
                from src.summary_formatter import SummaryFormatter
                formatter = SummaryFormatter()
                
                output = formatter.format(summary, 'markdown')
                print(output)
            else:
                logger.error("Failed to generate summary")
                return 1
        else:
            logger.info("No URL provided. Usage: python -m src.main <url>")
            print("Usage: python -m src.main <url>")
            print("Example: python -m src.main https://example.com/news")
            return 1
        
        return 0
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=DEBUG)
        return 1


if __name__ == '__main__':
    sys.exit(main())
