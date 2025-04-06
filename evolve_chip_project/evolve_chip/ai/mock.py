"""
モックAIクライアント

テストとデモ用のモックAIクライアント実装
"""

import time
from typing import Dict, Any, List, Optional

from .base import AIClientBase

class MockAIClient(AIClientBase):
    """
    モックAIクライアント
    
    テストとデモ用の擬似AIクライアント実装
    """
    
    def __init__(self, delay_seconds: float = 1.0):
        """
        モックAIクライアントの初期化
        
        Args:
            delay_seconds: 応答時の遅延秒数（デモ用）
        """
        self.delay_seconds = delay_seconds
    
    def generate_code_evolution(
        self, 
        source_code: str,
        goals: List[str],
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        モックのコード進化を生成
        
        Args:
            source_code: 元のソースコード
            goals: 進化の目標リスト
            constraints: 制約条件の辞書（オプション）
            
        Returns:
            進化後のコード情報
        """
        # 遅延を模倣（必要な場合）
        if self.delay_seconds > 0:
            time.sleep(self.delay_seconds)
        
        # ソースコードから関数名を抽出
        import re
        func_name_match = re.search(r'def\s+([a-zA-Z0-9_]+)', source_code)
        func_name = func_name_match.group(1) if func_name_match else "unknown_function"
        
        # 目標から何をすべきかを判断
        improved_code = ""
        explanation = ""
        
        if "readability" in goals:
            # 可読性向上の例
            if "HW" in source_code:
                # Hello Worldの短縮を修正
                improved_code = source_code.replace('print("HW")', 'print("Hello World")')
                explanation = "「HW」を「Hello World」に置き換えて可読性を向上させました。"
            else:
                # 既に改善されている場合はさらに改善
                improved_code = source_code.replace('print("Hello World")', 
                                              'message = "Hello World"\nprint(message)')
                explanation = "変数を導入して、コードの意図をより明確にしました。"
        
        elif "documentation" in goals:
            # ドキュメント化の例
            if '"""' not in source_code:
                # ドキュメントがない場合は追加
                doc_string = f'    """\n    {func_name}関数\n    \n    挨拶メッセージを表示します。\n    """\n'
                improved_code = re.sub(r'def\s+[a-zA-Z0-9_]+\([^)]*\):\s*', 
                                  lambda m: m.group(0) + doc_string, source_code)
                explanation = "関数にドキュメント文字列を追加しました。"
            else:
                # 既にドキュメントがある場合は強化
                improved_code = source_code
                explanation = "ドキュメントは既に十分です。"
        
        else:
            # デフォルトの進化
            improved_code = f"""def {func_name}(name: str = "World") -> str:
    \"\"\"
    カスタマイズ可能な挨拶メッセージを生成する関数
    
    Args:
        name: 挨拶の対象となる名前（デフォルト: "World"）
        
    Returns:
        生成された挨拶メッセージ
    \"\"\"
    message = f"Hello {{name}}"
    print(message)
    return message
"""
            explanation = "型ヒント、カスタマイズ機能、戻り値を追加して関数を改善しました。"
        
        return {
            'success': True,
            'evolved_code': improved_code,
            'explanation': explanation
        }

    def generate_content(self, prompt: str) -> str:
        """プロンプトからコンテンツを生成（モック）"""
        time.sleep(self.delay_seconds)
        return "def greet():\n    print('Hello World')"
    
    def chat(self, messages: list) -> str:
        """チャット形式でコンテンツを生成（モック）"""
        time.sleep(self.delay_seconds)
        return "Hello World"
    
    def embed(self, text: str) -> list:
        """テキストをベクトルに変換（モック）"""
        time.sleep(self.delay_seconds)
        return [0.1, 0.2, 0.3] 