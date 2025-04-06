"""
進化デコレータ

コードの意図を進化させるデコレータを提供します。
"""

import functools
import inspect
from enum import Enum
from typing import List, Dict, Any, Callable, Optional

class EvolutionGoal(Enum):
    """進化の目標を定義する列挙型"""
    READABILITY = "readability"  # コードの可読性を向上
    PERFORMANCE = "performance"  # パフォーマンスを改善

def evolve(
    goals: Optional[List[EvolutionGoal]] = None,
    constraints: Optional[Dict[str, str]] = None
):
    """
    コードを進化させるデコレータ
    
    Args:
        goals: 進化の目標リスト
        constraints: 制約条件の辞書
        
    Example:
        @evolve(
            goals=[EvolutionGoal.READABILITY],
            constraints={'output': 'Hello World'}
        )
        def greet():
            print("HW")  # AIが"Hello World"に進化
    """
    goals = goals or [EvolutionGoal.READABILITY]
    constraints = constraints or {}
    
    def decorator(func: Callable) -> Callable:
        # 進化用のメタデータを設定
        func.goals = goals
        func.constraints = constraints
        
        # ソースコードを取得
        try:
            func.source = inspect.getsource(func)
        except Exception:
            # フォールバック：関数定義を文字列として生成
            args = inspect.getfullargspec(func).args
            args_str = ", ".join(args)
            func.source = f"def {func.__name__}({args_str}):\n    {func.__doc__ or ''}\n    pass"
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
            
        return wrapper
        
    return decorator

def generate_prompt(func: Callable) -> str:
    """
    AIに渡すプロンプトを生成
    
    Args:
        func: 進化対象の関数
        
    Returns:
        生成されたプロンプト
    """
    code = func.source
    goals = ", ".join(g.value for g in func.goals)
    
    # 制約の詳細な説明を生成
    constraints_text = ""
    for k, v in func.constraints.items():
        if k == 'output':
            constraints_text += f"- 出力は正確に「{v}」と一致する必要があります\n"
        elif k == 'memory':
            constraints_text += f"- メモリ使用量は{v}以下に抑える必要があります\n"
        elif k == 'runtime':
            constraints_text += f"- 実行時間は{v}以下である必要があります\n"
        elif k == 'cpu':
            constraints_text += f"- CPU使用率は{v}以下に抑える必要があります\n"
        else:
            constraints_text += f"- {k}: {v}\n"
    
    # プロンプトの生成
    return f"""あなたは熟練したPythonエンジニアです。以下のコードを改善してください：

```python
{code}
```

改善の目標：
{goals}の観点から改善を行ってください。

制約条件：
{constraints_text}

以下の点に注意して改善を行ってください：
1. コードの可読性を高める
   - 適切な変数名を使用
   - 明確なコメントを追加
   - Pythonのドキュメント文字列を使用
2. Pythonのベストプラクティスに従う
   - PEP 8スタイルガイドに準拠
   - 適切な型ヒントを使用
   - 効率的なデータ構造を選択
3. エラー処理を適切に実装
   - 例外処理を追加
   - エッジケースを考慮
4. 制約条件を厳密に守る
   - 出力形式を遵守
   - リソース制限を遵守

改善したコードを単一のPythonコードブロックとして提供してください：
```python
# ここに改善したコードを記述
```

注意：コードブロック以外の説明は不要です。""" 