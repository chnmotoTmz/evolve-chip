from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class CodeGoal(Enum):
    """コード改善の目標"""
    READABILITY = "readability"
    PERFORMANCE = "performance"
    SECURITY = "security"

@dataclass
class CodeSuggestion:
    """コード改善の提案"""
    description: str
    priority: int
    impact: float
    code_example: Optional[str] = None

def analyze_code(code: str, goals: List[CodeGoal]) -> List[CodeSuggestion]:
    """コードを分析し、改善提案を生成する"""
    suggestions = []
    
    if "print(" in code:
        suggestions.append(
            CodeSuggestion(
                description="print文をloggingに置き換えることを推奨します",
                priority=1,
                impact=0.5,
                code_example="import logging\nlogging.info('message')"
            )
        )
    
    if "def " in code and "->" not in code:
        suggestions.append(
            CodeSuggestion(
                description="関数に戻り値の型ヒントを追加することを推奨します",
                priority=2,
                impact=0.3,
                code_example="def function() -> str:"
            )
        )
    
    suggestions.sort(key=lambda x: x.priority)
    return suggestions 