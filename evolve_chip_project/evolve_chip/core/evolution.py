"""
進化の中核機能

コードの進化を管理する中核機能を提供します。
"""

import os
import ast
import inspect
import logging
from typing import Dict, Any, List, Optional, Callable
from enum import Enum

from evolve_chip.ai import AIClientBase, MockAIClient

logger = logging.getLogger(__name__)

class EvolutionGoal(Enum):
    """進化の目標を定義する列挙型"""
    READABILITY = "readability"       # コードの可読性向上
    PERFORMANCE = "performance"       # パフォーマンス最適化
    MEMORY = "memory"                 # メモリ使用量の最適化
    TYPE_SAFETY = "type_safety"       # 型安全性の向上
    DOCUMENTATION = "documentation"   # ドキュメント品質向上

class Evolution:
    """
    コード進化を管理するクラス
    
    コードの解析、制約の検証、進化の実行を管理します。
    """
    
    def __init__(
        self,
        goals: List[EvolutionGoal],
        constraints: Optional[Dict[str, Any]] = None,
        ai_client: Optional[AIClientBase] = None
    ):
        """
        進化マネージャーの初期化
        
        Args:
            goals: 進化の目標リスト
            constraints: 制約条件（オプション）
            ai_client: AIクライアント（オプション）
        """
        self.goals = goals
        self.constraints = constraints or {}
        self.ai_client = ai_client or MockAIClient(delay_seconds=1.0)
        
    def analyze_code(self, func: Callable) -> Dict[str, Any]:
        """
        コードを解析し、特徴を抽出
        
        Args:
            func: 解析対象の関数
            
        Returns:
            コードの特徴を含む辞書
        """
        source = inspect.getsource(func)
        tree = ast.parse(source)
        
        # コードの特徴を抽出
        features = {
            'name': func.__name__,
            'doc': func.__doc__,
            'args': list(inspect.signature(func).parameters.keys()),
            'returns': inspect.signature(func).return_annotation,
            'source': source,
            'ast': tree
        }
        
        return features
    
    def validate_constraints(self, func: Callable, strict: bool = False) -> bool:
        """
        制約条件を検証
        
        Args:
            func: 検証対象の関数
            strict: 厳格モード（Trueの場合、制約違反で失敗）
            
        Returns:
            制約を満たしているかどうか
        """
        if not self.constraints:
            return True
            
        all_constraints_satisfied = True
            
        # メモリ制約の検証
        if 'memory' in self.constraints:
            import psutil
            process = psutil.Process()
            before = process.memory_info().rss
            func()
            after = process.memory_info().rss
            memory_used = (after - before) / 1024 / 1024  # MB
            
            limit = float(self.constraints['memory'].replace('< ', '').replace('MB', ''))
            if memory_used > limit:
                logger.warning(f"メモリ制約違反: {memory_used}MB > {limit}MB")
                all_constraints_satisfied = False
        
        # 出力制約の検証
        if 'output' in self.constraints:
            import io
            from contextlib import redirect_stdout
            
            f = io.StringIO()
            with redirect_stdout(f):
                func()
            actual_output = f.getvalue().strip()
            
            if actual_output != self.constraints['output']:
                logger.warning(f"出力制約違反: '{actual_output}' != '{self.constraints['output']}'")
                all_constraints_satisfied = False
        
        # 厳格モードでない場合は警告のみ
        if not all_constraints_satisfied and strict:
            logger.error("制約条件を満たしていません")
            return False
            
        return True
    
    def apply_evolution(self, func: Callable, strict_constraints: bool = False) -> Optional[str]:
        """
        進化を適用
        
        Args:
            func: 進化対象の関数
            strict_constraints: 制約の厳格チェック（デフォルトはFalse）
            
        Returns:
            進化後のコード、または失敗時はNone
        """
        # コードを解析
        features = self.analyze_code(func)
        
        # 制約を検証（厳格でないモード）
        self.validate_constraints(func, strict=strict_constraints)
        
        # 目標リストを文字列に変換
        goals_str = [g.value for g in self.goals]
        
        # AIクライアントを使用して進化を生成
        logger.info(f"AIを使用して進化を生成中: {', '.join(goals_str)}")
        result = self.ai_client.generate_code_evolution(
            source_code=features['source'],
            goals=goals_str,
            constraints=self.constraints
        )
        
        if not result.get('success'):
            logger.error("進化の生成に失敗しました")
            return None
            
        logger.info(f"進化が完了しました: {result.get('explanation')}")
        return result.get('evolved_code') 