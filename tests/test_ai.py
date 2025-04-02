import pytest
from evolve_chip import EvolutionGoal, EvolutionSuggestion
from evolve_chip.ai.engine import AIEngine, DefaultAIEngine

def test_ai_engine_base():
    """AIEngineの基本クラステスト"""
    engine = AIEngine()
    assert engine.model_name == "default"
    
    # 抽象メソッドのテスト
    suggestions = engine.analyze("test", [EvolutionGoal.READABILITY], [])
    assert isinstance(suggestions, list)

def test_default_ai_engine():
    """DefaultAIEngineのテスト"""
    engine = DefaultAIEngine()
    
    # print文を含むコードのテスト
    code_with_print = """
def test_function():
    print("test")
    return True
"""
    suggestions = engine.analyze(code_with_print, [EvolutionGoal.READABILITY], [])
    assert len(suggestions) > 0
    assert any(s.title == "ロギング改善" for s in suggestions)
    
    # 型ヒントなしの関数のテスト
    code_without_type_hints = """
def test_function(a, b):
    return a + b
"""
    suggestions = engine.analyze(code_without_type_hints, [EvolutionGoal.READABILITY], [])
    assert len(suggestions) > 0
    assert any(s.title == "戻り値の型ヒント追加" for s in suggestions)

def test_suggestion_priority():
    """提案の優先順位テスト"""
    engine = DefaultAIEngine()
    code = """
def test_function():
    print("test")
    return True
"""
    suggestions = engine.analyze(code, [EvolutionGoal.READABILITY], [])
    
    # 提案が存在することを確認
    assert len(suggestions) > 0
    
    # 優先順位の順序を確認
    priorities = [s.priority for s in suggestions]
    assert priorities == sorted(priorities) 