from dataclasses import dataclass
from typing import List, Optional

@dataclass
class EvolutionSuggestion:
    """
    コード進化の提案を表現するデータクラス
    """
    title: str                  # 提案タイトル
    description: str            # 提案の詳細説明
    code_sample: str            # 提案されたコードサンプル
    priority: int = 1           # 優先度(1-5, 1が最高)
    impact: str = "medium"      # 影響度(high/medium/low)
    goals: List[str] = None     # 対応する進化目標
    
    def __post_init__(self):
        if self.goals is None:
            self.goals = []
            
    def to_dict(self):
        """辞書形式に変換"""
        return {
            "title": self.title,
            "description": self.description,
            "code_sample": self.code_sample,
            "priority": self.priority,
            "impact": self.impact,
            "goals": self.goals
        }
    
    @classmethod
    def from_dict(cls, data):
        """辞書から作成"""
        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            code_sample=data.get("code_sample", ""),
            priority=data.get("priority", 1),
            impact=data.get("impact", "medium"),
            goals=data.get("goals", [])
        ) 