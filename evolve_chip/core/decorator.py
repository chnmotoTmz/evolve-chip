import os
import functools
from typing import List, Optional, Any, Callable
from .chip import EvolveChip

def evolve(
    goals: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
    ai_engine: Optional[Any] = None,
    instructions: Optional[str] = None
) -> Callable:
    """
    AIチップを関数に適用するデコレータ
    
    Args:
        goals: 進化の目標リスト
        constraints: 制約条件リスト
        ai_engine: カスタムAIエンジン
        instructions: AIに与える具体的な指示（例: "関数を中国語対応にする"）
    
    Returns:
        デコレートされた関数
    """
    def decorator(func: Callable) -> Callable:
        if os.environ.get("EVOLVE_MODE") == "development":
            return EvolveChip(func, goals, constraints, ai_engine, instructions)
        return func
    return decorator 