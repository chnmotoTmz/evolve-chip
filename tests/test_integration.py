import os
import pytest
from evolve_chip import evolve, EvolutionGoal, DefaultAIEngine

def test_full_evolution_cycle():
    """完全な進化サイクルのテスト"""
    # AIエンジンの作成
    ai_engine = DefaultAIEngine()
    
    # テスト用の関数
    @evolve(
        goals=[EvolutionGoal.READABILITY, EvolutionGoal.PERFORMANCE],
        ai_engine=ai_engine
    )
    def test_function(a: int, b: int):
        print(f"Calculating sum of {a} and {b}")
        return a + b
    
    # 開発モードで実行
    os.environ["EVOLVE_MODE"] = "development"
    result = test_function(5, 3)
    assert result == 8
    
    # 本番モードで実行
    os.environ["EVOLVE_MODE"] = "production"
    result = test_function(5, 3)
    assert result == 8

def test_multiple_functions():
    """複数関数のテスト"""
    ai_engine = DefaultAIEngine()
    
    @evolve(
        goals=[EvolutionGoal.READABILITY],
        ai_engine=ai_engine
    )
    def function1():
        print("Function 1")
        return True
    
    @evolve(
        goals=[EvolutionGoal.PERFORMANCE],
        ai_engine=ai_engine
    )
    def function2():
        print("Function 2")
        return False
    
    # 開発モードで実行
    os.environ["EVOLVE_MODE"] = "development"
    assert function1() is True
    assert function2() is False 