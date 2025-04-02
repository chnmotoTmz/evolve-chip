import os
import pytest
from evolve_chip import evolve, EvolutionGoal, EvolutionSuggestion
from evolve_chip.core.chip import EvolveChip

def test_evolution_goal_enum():
    """EvolutionGoalの列挙型テスト"""
    assert EvolutionGoal.READABILITY.value == "readability"
    assert EvolutionGoal.PERFORMANCE.value == "performance"
    assert EvolutionGoal.SECURITY.value == "security"
    assert EvolutionGoal.MAINTAINABILITY.value == "maintainability"

def test_evolution_suggestion():
    """EvolutionSuggestionのデータクラステスト"""
    suggestion = EvolutionSuggestion(
        title="テスト提案",
        description="テスト用の提案",
        code_sample="print('test')",
        priority=1,
        impact="high"
    )
    assert suggestion.title == "テスト提案"
    assert suggestion.description == "テスト用の提案"
    assert suggestion.code_sample == "print('test')"
    assert suggestion.priority == 1
    assert suggestion.impact == "high"

def test_evolve_decorator():
    """evolveデコレータのテスト"""
    @evolve(goals=[EvolutionGoal.READABILITY])
    def test_function():
        print("test")
    
    # 開発モードで実行
    os.environ["EVOLVE_MODE"] = "development"
    test_function()
    
    # 本番モードで実行
    os.environ["EVOLVE_MODE"] = "production"
    test_function()

def test_evolve_chip_initialization():
    """EvolveChipの初期化テスト"""
    def test_func():
        pass
    
    chip = EvolveChip(test_func)
    assert chip.func == test_func
    assert chip.func_name == "test_func"
    assert EvolutionGoal.READABILITY in chip.goals
    assert EvolutionGoal.PERFORMANCE in chip.goals
    assert "preserve_semantics" in chip.constraints 