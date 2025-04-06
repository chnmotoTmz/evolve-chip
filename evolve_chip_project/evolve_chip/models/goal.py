from enum import Enum

class EvolutionGoal(Enum):
    """コード改善の目標を表す列挙型"""
    READABILITY = "readability"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    TESTABILITY = "testability"
    
    @classmethod
    def from_string(cls, value: str):
        """文字列から列挙型を取得"""
        for goal in cls:
            if goal.value.lower() == value.lower():
                return goal
        raise ValueError(f"不明な進化目標: {value}")
    
    def __str__(self):
        return self.value 