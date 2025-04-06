"""
シンプルなオーケストレータ

@evolveデコレータ付きの関数を抽出し、進化を実行します。
"""

import ast
import os
import logging
from typing import Dict, Any
from core.decorators import evolve, generate_prompt
from constraints.checker import check_output, check_resource_constraints
from ai.factory import create_ai_client

logger = logging.getLogger(__name__)

class SimpleOrchestrator:
    """
    シンプルなオーケストレータ
    
    単一のPythonファイルから@evolveデコレータ付きの関数を抽出し、
    AIを使用して進化を実行します。
    """
    
    def __init__(self, file_path: str):
        """
        初期化
        
        Args:
            file_path: 進化させるPythonファイルのパス
        """
        self.file_path = file_path
        self.globals = {}
        
        # ファイルを読み込み
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                exec(f.read(), self.globals)
        except Exception as e:
            logger.error(f"ファイルの読み込みに失敗: {e}")
            raise
        
        # AIクライアントの初期化
        try:
            self.ai_client = create_ai_client(
                provider="gemini" if os.environ.get("GEMINI_API_KEY") else "mock"
            )
        except Exception as e:
            logger.error(f"AIクライアントの初期化に失敗: {e}")
            raise

    def extract_evolve_functions(self) -> Dict[str, Any]:
        """
        @evolveデコレータ付きの関数を抽出
        
        Returns:
            関数名と関数オブジェクトの辞書
        """
        functions = {}
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func = self.globals.get(node.name)
                    if func and hasattr(func, 'goals'):
                        functions[node.name] = func
        except Exception as e:
            logger.error(f"関数の抽出に失敗: {e}")
            raise
            
        return functions

    def evolve_code(self):
        """
        進化を実行し、結果を保存
        
        各関数に対して：
        1. プロンプトを生成
        2. AIからコード提案を取得
        3. 制約チェック
        4. 進化後のコードを保存
        """
        funcs = self.extract_evolve_functions()
        if not funcs:
            logger.warning("進化対象の関数が見つかりません")
            return
            
        for name, func in funcs.items():
            try:
                # プロンプト生成
                prompt = generate_prompt(func)
                logger.info(f"Generated prompt for {name}:\n{prompt}")
                
                # AIからコード提案を取得
                evolved_code = self.ai_client.generate_content(prompt)
                logger.info(f"Generated code for {name}:\n{evolved_code}")
                
                # コードブロックの抽出（もしあれば）
                if "```python" in evolved_code:
                    evolved_code = evolved_code.split("```python")[1].split("```")[0].strip()
                
                # 進化後のコードを保存
                output_path = os.path.join(os.path.dirname(self.file_path), "v2_evolved.py")
                with open(output_path, "w", encoding='utf-8') as f:
                    f.write(evolved_code)
                logger.info(f"Evolved code saved to {output_path}")
                
                # 制約チェック
                exec(evolved_code, self.globals)
                evolved_func = self.globals[name]
                output_ok = check_output(evolved_func, func.constraints.get('output', ''))
                memory_ok, runtime_ok, cpu_ok = check_resource_constraints(evolved_func, func.constraints)
                logger.info(
                    f"Constraints check for {name}:\n"
                    f"- Output: {'✓' if output_ok else '✗'}\n"
                    f"- Memory: {'✓' if memory_ok else '✗'}\n"
                    f"- Runtime: {'✓' if runtime_ok else '✗'}\n"
                    f"- CPU: {'✓' if cpu_ok else '✗'}"
                )
                
            except Exception as e:
                logger.error(f"Error evolving {name}: {e}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    orchestrator = SimpleOrchestrator("examples/hello_world/v1_initial.py")
    orchestrator.evolve_code() 