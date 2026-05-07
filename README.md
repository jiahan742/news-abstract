# 新闻摘要助手 (News Abstract Assistant)

一个智能新闻摘要生成工具，能够识别网页链接中的新闻内容（支持全球各地的语言），并自动生成结构化摘要。

## ✨ 核心功能

- 🌐 **多语言支持** - 自动识别并处理全球各地的语言内容（英文、中文、日文、韩文等）
- 🔗 **网页链接识别** - 自动爬取和解析网页中的新闻内容
- 📝 **智能摘要生成** - 提取新闻的核心信息，包括：
  - **角色** (Who) - 涉及的人物、组织或机构
  - **时间** (When) - 事件发生的时间
  - **事件** (What) - 具体发生了什么
  - **结果** (Result) - 事件的后果或影响

## 📦 项目结构

```
news-abstract/
├── src/
│   ├── __init__.py
│   ├── main.py                 # 主程序入口
│   ├── news_fetcher.py        # 新闻网页爬取模块
│   ├── language_detector.py    # 语言检测模块
│   ├── content_extractor.py    # 内容提取模块
│   ├── abstract_generator.py   # 摘要生成模块
│   └── summary_formatter.py    # 摘要格式化模块
├── tests/
│   ├── __init__.py
│   └── test_abstract.py
├── requirements.txt
├── config.py
├── .gitignore
└── README.md
```

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基本使用

```python
from src.abstract_generator import NewsAbstractGenerator

# 初始化生成器
generator = NewsAbstractGenerator()

# 处理新闻链接
url = "https://example.com/news/article"
summary = generator.process_url(url)

# 输出结构化摘要
print(summary)
```

### 输出示例

```json
{
  "title": "新闻标题",
  "original_language": "zh",
  "summary": {
    "characters": ["人物A", "人物B", "组织X"],
    "time": "2026年5月7日",
    "event": "具体发生的事件描述",
    "result": "事件的结果和影响"
  },
  "source_url": "https://example.com/news/article",
  "processed_at": "2026-05-07T10:30:00Z"
}
```

## 🔧 核心模块说明

### news_fetcher.py
- 使用 `requests` 和 `beautifulsoup4` 爬取网页内容
- 处理各种网页编码格式
- 提取新闻正文和元数据

### language_detector.py
- 使用 `langdetect` 或 `textblob` 自动检测文本语言
- 支持20+种语言

### content_extractor.py
- 提取网页中的主要新闻内容
- 移除广告、导航等无关内容
- 保留新闻的结构化信息

### abstract_generator.py
- 使用 NLP 技术（如 `transformers` 或 `spacy`）进行文本分析
- 智能提取四个必要元素：角色、时间、事件、结果
- 生成简洁的摘要文本

### summary_formatter.py
- 格式化摘要为 JSON、Markdown 等格式
- 支持多语言输出

## 📋 依赖包

- `requests` - HTTP 请求库
- `beautifulsoup4` - HTML 解析
- `langdetect` - 语言检测
- `transformers` - NLP 模型
- `spacy` - 自然语言处理
- `python-dateutil` - 时间处理
- `pytest` - 测试框架

## 🧪 测试

```bash
pytest tests/
```

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请通过 GitHub Issues 联系我们。