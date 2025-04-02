from typing import List, Optional
from abc import ABC, abstractmethod

from .client import get_ai_client
from ..models.suggestion import EvolutionSuggestion
from ..models.goal import EvolutionGoal

class AIEngine(ABC):
    @abstractmethod
    def analyze(
        self,
        code: str,
        goals: List[EvolutionGoal],
        constraints: Optional[List[str]] = None
    ) -> List[EvolutionSuggestion]:
        """コードを分析して改善提案を生成する"""
        pass
    
    @abstractmethod
    def analyze_with_instructions(
        self,
        code: str,
        instructions: str,
        goals: List[EvolutionGoal],
        constraints: Optional[List[str]] = None
    ) -> List[EvolutionSuggestion]:
        """指示に基づいてコードを分析・変更する"""
        pass

class DefaultAIEngine(AIEngine):
    def __init__(self):
        self.ai_client = get_ai_client()
    
    def analyze(
        self,
        code: str,
        goals: List[EvolutionGoal],
        constraints: Optional[List[str]] = None
    ) -> List[EvolutionSuggestion]:
        """コードを分析して改善提案を生成する"""
        try:
            response = self.ai_client.analyze_code(code, goals, constraints)
            return response.suggestions
        except Exception:
            return []
    
    def analyze_with_instructions(
        self,
        code: str,
        instructions: str,
        goals: List[EvolutionGoal],
        constraints: Optional[List[str]] = None
    ) -> List[EvolutionSuggestion]:
        """指示に基づいてコードを分析・変更する"""
        try:
            response = self.ai_client.execute_instructions(code, instructions, goals, constraints)
            return response.suggestions
        except Exception as e:
            print(f"指示の実行中にエラーが発生しました: {e}")
            return [] 