from dataclasses import dataclass
from typing import Optional

@dataclass
class EvolutionSuggestion:
    """コード改善の提案を表すデータクラス"""
    title: str = ""
    description: str = ""
    code_sample: str = ""
    priority: int = 1
    impact: str = "medium"
    # 互換性のための別名
    @property
    def code_example(self) -> str:
        return self.code_sample 