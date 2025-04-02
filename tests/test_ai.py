import pytest
from evolve_chip import EvolutionGoal, EvolutionSuggestion
from evolve_chip.ai.engine import AIEngine, DefaultAIEngine
from typing import List, Optional

class TestAIEngine(AIEngine):
    """テスト用のAIEngine実装"""
    def analyze(
        self,
        code: str,
        goals: List[EvolutionGoal],
        constraints: Optional[List[str]] = None
    ) -> List[EvolutionSuggestion]:
        return []

def test_ai_engine_base():
    """AIEngineの基本クラステスト"""
    engine = TestAIEngine()
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
    assert any("print文" in s.description for s in suggestions)
    
    # 型ヒントなしの関数のテスト
    code_without_type_hints = """
def test_function(a, b):
    return a + b
"""
    suggestions = engine.analyze(code_without_type_hints, [EvolutionGoal.READABILITY], [])
    assert len(suggestions) > 0
    assert any("型ヒント" in s.description for s in suggestions)

def test_suggestion_priority():
    """提案の優先順位テスト"""
    engine = DefaultAIEngine()
    code = """
def test_function():
    print("test")
    return True
"""
    suggestions = engine.analyze(code, [EvolutionGoal.READABILITY], [])
    assert len(suggestions) > 0
    priorities = [s.priority for s in suggestions]
    assert priorities == sorted(priorities) 