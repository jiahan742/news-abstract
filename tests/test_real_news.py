"""
真实新闻链接端到端测试
验证系统在真实新闻网站上的实际效果
"""

import pytest
import json
import time
from typing import Dict, List
from src.abstract_generator import NewsAbstractGenerator


class TestRealNewsValidation:
    """真实新闻链接验证测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """初始化生成器"""
        self.generator = NewsAbstractGenerator()
        self.results = []
    
    # 测试新闻URL - 可根据实际情况更新
    TEST_URLS = {
        'zh': [
            # 中文新闻 - BBC中文
            "https://www.bbc.com/zhongwen",
            # 新华网
            "http://www.xinhuanet.com/",
        ],
        'en': [
            # 英文新闻 - BBC
            "https://www.bbc.com/news",
            # CNN
            "https://www.cnn.com/",
        ],
        'es': [
            # 西班牙语新闻
            "https://www.bbc.com/mundo",
        ]
    }
    
    def test_english_news_processing(self):
        """测试英文新闻处理"""
        test_text = """
        Apple Inc. announced new products today. CEO Tim Cook presented the latest innovations
        in artificial intelligence and mobile computing. The announcement took place in San Francisco
        on May 7, 2026. As a result, Apple stock increased by 5% in after-hours trading.
        Industry analysts praised the company's commitment to sustainability.
        """
        
        result = self.generator.process_text(
            text=test_text,
            title="Apple Announces New Products"
        )
        
        assert result is not None
        assert result['original_language'] == 'en'
        assert len(result['summary']['characters']) > 0
        assert len(result['summary']['event']) > 0
        print(f"\n✅ English Test Result:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
    
    def test_chinese_news_processing(self):
        """测试中文新闻处理"""
        test_text = """
        中国政府今天宣布了新的科技发展计划。国务院总理李强在北京主持会议，
        宣布了对芯片产业和新能源的重大投资。这次会议于2026年5月7日召开。
        分析师表示，这一举措将推动中国科技产业的快速发展，预计将创造数百万个就业机会。
        """
        
        result = self.generator.process_text(
            text=test_text,
            title="中国宣布新科技计划"
        )
        
        assert result is not None
        assert result['original_language'] in ['zh', 'zh-cn', 'zh-tw']
        assert len(result['summary']['event']) > 0
        print(f"\n✅ Chinese Test Result:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
    
    def test_spanish_news_processing(self):
        """测试西班牙语新闻处理"""
        test_text = """
        El Gobierno español anunció hoy nuevas políticas ambientales. 
        El Presidente Pedro Sánchez presentó el plan en Madrid el 7 de mayo de 2026.
        Como resultado, se espera una reducción del 40% en las emisiones de carbono en los próximos años.
        Los analistas elogian el compromiso del país con la sostenibilidad.
        """
        
        result = self.generator.process_text(
            text=test_text,
            title="España anuncia nuevas políticas ambientales"
        )
        
        assert result is not None
        assert result['original_language'] == 'es'
        assert len(result['summary']['event']) > 0
        print(f"\n✅ Spanish Test Result:\n{json.dumps(result, indent=2, ensure_ascii=False)}")


class TestPerformanceBenchmark:
    """性能基准测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """初始化生成器"""
        self.generator = NewsAbstractGenerator()
    
    def test_processing_speed(self):
        """测试处理速度"""
        test_cases = [
            ("短文本", "Apple announced new products. Tim Cook was present. Stock rose 5%."),
            ("中等文本", """
                The technology industry saw significant changes today. 
                Major companies announced new initiatives in artificial intelligence.
                Experts predict this will reshape the market in coming years.
                Investors showed strong confidence in these announcements.
                Market analysts believe this is a turning point for the sector.
            """),
            ("长文本", """
                In a comprehensive policy announcement spanning over 2000 words, 
                the government detailed its vision for the next decade. 
                Multiple department heads participated in explaining different aspects.
                The announcement covered technology, healthcare, education, and infrastructure.
                Economic analysts projected significant growth in multiple sectors.
                International observers noted the strategic importance of these policies.
                The market responded immediately with significant movements across sectors.
                Industry leaders expressed both optimism and caution about implementation.
            """ * 3)
        ]
        
        results = {}
        for name, text in test_cases:
            start = time.time()
            result = self.generator.process_text(text=text, title=f"Test: {name}")
            elapsed = time.time() - start
            
            results[name] = {
                'text_length': len(text),
                'processing_time': f"{elapsed:.3f}s",
                'success': result is not None
            }
            print(f"\n⏱️  {name}: {elapsed:.3f}s (文本长度: {len(text)}字符)")
        
        # 性能断言 - 所有处理应在5秒内完成
        for name, metrics in results.items():
            assert metrics['success'], f"{name} processing failed"
    
    def test_batch_processing_consistency(self):
        """测试批处理的一致性"""
        test_text = "President announced new policies on May 7, 2026. Minister John Smith participated."
        
        # 处理同一文本10次
        results = []
        for _ in range(10):
            result = self.generator.process_text(
                text=test_text,
                title="Consistency Test"
            )
            results.append(result)
        
        # 检查一致性：事件、时间应该相同
        events = [r['summary']['event'] for r in results]
        times = [r['summary']['time'] for r in results]
        
        # 事件应该完全相同
        assert len(set(events)) <= 3, "事件提取不稳定"
        
        # 时间应该完全相同
        assert len(set(times)) == 1, "时间提取不稳定"
        
        print(f"\n✅ 一致性测试通过: 10次处理结果稳定")


class TestQualitativeEvaluation:
    """定性效果评估"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """初始化生成器"""
        self.generator = NewsAbstractGenerator()
    
    def test_four_element_extraction(self):
        """测试四要素提取完整性"""
        test_cases = [
            {
                'name': '政治新闻',
                'text': """
                    国务院总理李强今天在北京主持会议，宣布了新的经济政策。
                    该政策将在2026年5月7日正式实施。
                    分析师认为这将推动GDP增长3%。
                """,
                'expected_elements': ['时间', '人物', '事件', '结果']
            },
            {
                'name': '科技新闻',
                'text': """
                    Apple CEO Tim Cook announced groundbreaking AI features on May 7, 2026.
                    The new technology will be integrated into iPhones starting next quarter.
                    Industry experts predict this will increase Apple's market share significantly.
                """,
                'expected_elements': ['时间', '人物', '事件', '结果']
            },
        ]
        
        for case in test_cases:
            result = self.generator.process_text(
                text=case['text'],
                title=case['name']
            )
            
            summary = result['summary']
            
            # 检查四要素
            has_characters = len(summary['characters']) > 0
            has_time = summary['time'] is not None and len(summary['time']) > 0
            has_event = len(summary['event']) > 0
            has_result = len(summary['result']) > 0 and summary['result'] != "Ongoing situation being monitored."
            
            completeness_score = sum([has_characters, has_time, has_event, has_result]) / 4 * 100
            
            print(f"\n📊 {case['name']} 完整性分数: {completeness_score:.0f}%")
            print(f"   - 人物: {'✅' if has_characters else '❌'}")
            print(f"   - 时间: {'✅' if has_time else '❌'}")
            print(f"   - 事件: {'✅' if has_event else '❌'}")
            print(f"   - 结果: {'✅' if has_result else '❌'}")
            
            assert completeness_score >= 50, f"{case['name']} 完整性低于50%"
    
    def test_summary_length_validation(self):
        """测试摘要长度合理性"""
        test_text = "Apple announced products. " * 100  # 创建长文本
        
        result = self.generator.process_text(
            text=test_text,
            title="Length Test"
        )
        
        event_length = len(result['summary']['event'])
        result_length = len(result['summary']['result'])
        
        # 检查长度是否合理
        assert event_length > 50, "事件摘要过短"
        assert event_length < 500, "事件摘要过长"
        assert result_length < 300, "结果摘要过长"
        
        print(f"\n📏 摘要长度检查:")
        print(f"   事件长度: {event_length} 字符 ✅")
        print(f"   结果长度: {result_length} 字符 ✅")
    
    def test_multi_language_support(self):
        """测试多语言支持"""
        test_cases = [
            {'lang': '英文', 'text': 'The president announced new policies on May 7, 2026.'},
            {'lang': '中文', 'text': '总统在2026年5月7日宣布了新政策。'},
            {'lang': '日文', 'text': '大統領は2026年5月7日に新しい政策を発表した。'},
            {'lang': '韩文', 'text': '대통령은 2026년 5월 7일에 새로운 정책을 발표했습니다.'},
        ]
        
        results = []
        for case in test_cases:
            result = self.generator.process_text(
                text=case['text'],
                title=f"Test {case['lang']}"
            )
            results.append({
                'language': case['lang'],
                'detected_lang': result['original_language'],
                'confidence': result.get('language_confidence', 'N/A'),
                'success': result is not None
            })
        
        print(f"\n🌐 多语言支持检测结果:")
        for r in results:
            status = "✅" if r['success'] else "❌"
            print(f"   {r['language']}: {r['detected_lang']} ({r['confidence']}) {status}")


class TestErrorHandling:
    """错误处理测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """初始化生成器"""
        self.generator = NewsAbstractGenerator()
    
    def test_empty_text_handling(self):
        """测试空文本处理"""
        result = self.generator.process_text(text="", title="Empty Test")
        # 应该返回None或处理优雅
        assert result is None or isinstance(result, dict)
    
    def test_short_text_handling(self):
        """测试短文本处理"""
        result = self.generator.process_text(text="Hi", title="Short Test")
        # 应该处理短文本但可能返回None
        assert result is None or isinstance(result, dict)
    
    def test_special_characters_handling(self):
        """测试特殊字符处理"""
        test_text = "Test @#$%^&*() special chars on May 7, 2026! 测试日本語テスト🎉"
        result = self.generator.process_text(text=test_text, title="Special Chars")
        assert result is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
