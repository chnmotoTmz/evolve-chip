from enum import Enum

class EvolutionGoal(Enum):
    """コード改善の目標を表す列挙型"""
    READABILITY = "readability"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    TESTABILITY = "testability" 