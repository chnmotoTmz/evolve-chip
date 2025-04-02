import os
import inspect
import functools
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum

class EvolutionGoal(Enum):
    READABILITY = "readability"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"

@dataclass
class EvolutionSuggestion:
    title: str
    description: str
    code_sample: str
    priority: int = 1
    impact: str = "medium"

class EvolveChip:
    def __init__(
        self,
        func: Any,
        goals: Optional[List[str]] = None,
        constraints: Optional[List[str]] = None,
        ai_engine: Optional[Any] = None,
        instructions: Optional[str] = None
    ):
        self.func = func
        self.goals = [EvolutionGoal(goal) for goal in (goals or ["readability", "performance"])]
        self.constraints = constraints or ["preserve_semantics"]
        self.original_source = inspect.getsource(func)
        self.func_name = func.__name__
        self.ai_engine = ai_engine
        self.instructions = instructions
        self.suggestions: List[EvolutionSuggestion] = []
        self.dev_mode = os.environ.get("EVOLVE_MODE") == "development"
        
        functools.update_wrapper(self, func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self.dev_mode:
            self._analyze()
        return self.func(*args, **kwargs)

    def _analyze(self) -> None:
        """コードを解析し、進化の提案を生成"""
        if self.ai_engine:
            # AIエンジンを使用した分析
            if self.instructions:
                # 指示がある場合は指示に基づく分析を実行
                self._analyze_with_instructions()
            else:
                # 通常の品質分析を実行
                self.suggestions = self.ai_engine.analyze(
                    self.original_source,
                    self.goals,
                    self.constraints
                )
        else:
            self._default_analysis()
        
        self._display_suggestions()
    
    def _analyze_with_instructions(self) -> None:
        """指示に基づいてコードを分析・変更する"""
        if not self.ai_engine:
            return
        
        try:
            # 指示に基づくコード変更の提案を生成
            self.suggestions = self.ai_engine.analyze_with_instructions(
                self.original_source,
                self.instructions,
                self.goals,
                self.constraints
            )
            print(f"\n指示「{self.instructions}」に基づく分析を実行しました\n")
        except Exception as e:
            print(f"指示の処理中にエラーが発生しました: {e}")
            self._default_analysis()

    def _default_analysis(self) -> None:
        """デフォルトの分析ロジック"""
        # 基本的なコードパターン分析
        if "Hello, World!" in self.original_source:
            self.suggestions = [
                EvolutionSuggestion(
                    title="ユーザー名入力",
                    description="ユーザー名を入力できるように変更",
                    code_sample="name = input('Your name: ') or 'World'; print(f'Hello, {name}!')",
                    priority=1
                ),
                EvolutionSuggestion(
                    title="時間帯挨拶",
                    description="時間帯に応じた挨拶に変更",
                    code_sample="import datetime; hour = datetime.datetime.now().hour; greeting = 'Good morning' if hour < 12 else 'Good afternoon' if hour < 18 else 'Good evening'; print(f'{greeting}, World!')",
                    priority=2
                )
            ]

    def _display_suggestions(self) -> None:
        """進化の提案を表示"""
        if not self.suggestions:
            return

        print(f"\nEvolveChip suggestions for {self.func_name}:")
        for i, suggestion in enumerate(sorted(self.suggestions, key=lambda x: x.priority), 1):
            print(f"{i}. {suggestion.title} (Priority: {suggestion.priority}, Impact: {suggestion.impact})")
            print(f"   {suggestion.description}")
            print(f"   Example: {suggestion.code_sample}")
        print("\n") 