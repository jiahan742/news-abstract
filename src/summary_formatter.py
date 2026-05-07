"""
摘要格式化模块

Responsible for:
- Formatting summaries into different output formats
- Supporting JSON, Markdown, and text output
- Multi-language support
"""

import json
import logging
from typing import Dict, Optional
from config import OUTPUT_FORMAT

logger = logging.getLogger(__name__)


class SummaryFormatter:
    """
    Formats summaries into different output formats
    """

    def __init__(self):
        self.supported_formats = ['json', 'markdown', 'text']
        self.default_format = OUTPUT_FORMAT

    def format_json(self, summary: Dict) -> str:
        """
        Format summary as JSON
        
        Args:
            summary: Summary dictionary
            
        Returns:
            JSON formatted string
        """
        return json.dumps(summary, ensure_ascii=False, indent=2)

    def format_markdown(self, summary: Dict) -> str:
        """
        Format summary as Markdown
        
        Args:
            summary: Summary dictionary
            
        Returns:
            Markdown formatted string
        """
        md = f"# {summary.get('title', 'News Summary')}\n\n"
        md += f"**Source:** [{summary.get('url', 'Unknown')}]({summary.get('url', '')})\n\n"
        md += f"**Language:** {summary.get('original_language', 'Unknown')}\n\n"
        
        if summary.get('publish_date'):
            md += f"**Published:** {summary['publish_date']}\n\n"
        
        md += "## 摘要 (Summary)\n\n"
        
        sum_data = summary.get('summary', {})
        
        if sum_data.get('characters'):
            md += f"### 角色 (Characters)\n"
            for char in sum_data['characters']:
                md += f"- {char}\n"
            md += "\n"
        
        if sum_data.get('time'):
            md += f"### 时间 (Time)\n{sum_data['time']}\n\n"
        
        if sum_data.get('event'):
            md += f"### 事件 (Event)\n{sum_data['event']}\n\n"
        
        if sum_data.get('result'):
            md += f"### 结果 (Result)\n{sum_data['result']}\n\n"
        
        md += f"---\n*Generated at: {summary.get('processed_at', 'Unknown')}*"
        
        return md

    def format_text(self, summary: Dict) -> str:
        """
        Format summary as plain text
        
        Args:
            summary: Summary dictionary
            
        Returns:
            Plain text formatted string
        """
        text = f"{summary.get('title', 'News Summary')}\n"
        text += f"{'=' * len(summary.get('title', 'News Summary'))}\n\n"
        
        if summary.get('url'):
            text += f"Source: {summary['url']}\n"
        
        if summary.get('original_language'):
            text += f"Language: {summary['original_language']}\n"
        
        if summary.get('publish_date'):
            text += f"Published: {summary['publish_date']}\n"
        
        text += "\n" + "-" * 50 + "\n\n"
        text += "SUMMARY\n"
        text += "-" * 50 + "\n\n"
        
        sum_data = summary.get('summary', {})
        
        if sum_data.get('characters'):
            text += "CHARACTERS:\n"
            for char in sum_data['characters']:
                text += f"  - {char}\n"
            text += "\n"
        
        if sum_data.get('time'):
            text += f"TIME: {sum_data['time']}\n\n"
        
        if sum_data.get('event'):
            text += f"EVENT:\n{sum_data['event']}\n\n"
        
        if sum_data.get('result'):
            text += f"RESULT:\n{sum_data['result']}\n"
        
        return text

    def format(self, summary: Dict, format_type: Optional[str] = None) -> str:
        """
        Format summary in specified format
        
        Args:
            summary: Summary dictionary
            format_type: Output format (json, markdown, text)
            
        Returns:
            Formatted summary string
        """
        fmt = format_type or self.default_format
        
        if fmt == 'json':
            return self.format_json(summary)
        elif fmt == 'markdown':
            return self.format_markdown(summary)
        elif fmt == 'text':
            return self.format_text(summary)
        else:
            logger.warning(f"Unknown format: {fmt}, using JSON")
            return self.format_json(summary)
