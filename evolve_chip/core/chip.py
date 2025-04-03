import os
import inspect
import functools
from typing import List, Optional, Any
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
        ai_engine: Any = None,
        instructions: Optional[str] = None
    ):
        self.func = func
        # 指定がない場合はデフォルトのゴールとして "readability" と "performance" を使用
        self.goals = [EvolutionGoal(goal) for goal in (goals if goals is not None else ["readability", "performance"])]
        # 制約がない場合は "preserve_semantics" を使用
        self.constraints = constraints if constraints is not None else ["preserve_semantics"]
        self.original_source = inspect.getsource(func)
        self.func_name = func.__name__
        # AIエンジンは必須とし、指定されていなければ例外を発生させる
        self.ai_engine = ai_engine
        if not self.ai_engine:
            raise Exception("AIエンジンが指定されていません。")
        self.instructions = instructions
        self.suggestions: List[EvolutionSuggestion] = []
        self.dev_mode = os.environ.get("EVOLVE_MODE") == "development"
        
        functools.update_wrapper(self, func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self.dev_mode:
            self._analyze()
        return self.func(*args, **kwargs)

    def _analyze(self) -> None:
        """
        コードを解析し、進化の提案を生成する。
        AIエンジンが設定されていない場合や、処理中に発生した例外はそのまま伝播する。
        """
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
        
        self._display_suggestions()

    def _analyze_with_instructions(self) -> None:
        """
        指示に基づいてコードを分析・変更する。
        AIエンジンを用いた処理でエラーが発生した場合は例外がそのまま伝播する。
        """
        self.suggestions = self.ai_engine.analyze_with_instructions(
            self.original_source,
            self.instructions,
            self.goals,
            self.constraints
        )
        print(f"\n指示「{self.instructions}」に基づく分析を実行しました\n")

    def _display_suggestions(self) -> None:
        """
        生成された進化の提案を表示する。
        提案が存在しない場合は何も出力しない。
        """
        if not self.suggestions:
            return

        print(f"\nEvolveChip suggestions for {self.func_name}:")
        for idx, suggestion in enumerate(sorted(self.suggestions, key=lambda s: s.priority), 1):
            print(f"{idx}. {suggestion.title} (Priority: {suggestion.priority}, Impact: {suggestion.impact})")
            print(f"   {suggestion.description}")
            print(f"   Example: {suggestion.code_sample}")
        print("\n")
