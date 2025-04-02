import ast
from typing import List, Optional, Any, Dict
from dataclasses import dataclass
from ..core.chip import EvolutionSuggestion

@dataclass
class ASTNodeInfo:
    """ASTノードの情報を保持するデータクラス"""
    node_type: str
    line_number: int
    column: int
    parent_type: Optional[str] = None
    children: List[str] = None

class ASTAnalyzer:
    """ASTを解析し、コードの構造を理解するクラス"""
    
    def __init__(self, source_code: str):
        self.tree = ast.parse(source_code)
        self.node_info: List[ASTNodeInfo] = []
        self._analyze_tree()

    def _analyze_tree(self) -> None:
        """ASTツリーを解析し、ノード情報を収集"""
        for node in ast.walk(self.tree):
            info = ASTNodeInfo(
                node_type=type(node).__name__,
                line_number=getattr(node, 'lineno', 0),
                column=getattr(node, 'col_offset', 0),
                children=[type(child).__name__ for child in ast.iter_child_nodes(node)]
            )
            self.node_info.append(info)

    def find_function_definitions(self) -> List[Dict[str, Any]]:
        """関数定義を探す"""
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'returns': ast.unparse(node.returns) if node.returns else None,
                    'line': node.lineno
                })
        return functions

    def find_print_statements(self) -> List[Dict[str, Any]]:
        """print文を探す"""
        prints = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
                prints.append({
                    'args': [ast.unparse(arg) for arg in node.args],
                    'line': node.lineno
                })
        return prints

class CodeTransformer:
    """コード変換を行うクラス"""
    
    @staticmethod
    def add_type_hints(source_code: str, function_name: str, param_types: Dict[str, str], return_type: str) -> str:
        """関数に型ヒントを追加"""
        tree = ast.parse(source_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                # 引数の型ヒントを追加
                for arg in node.args.args:
                    if arg.arg in param_types:
                        arg.annotation = ast.parse(param_types[arg.arg]).body[0].value
                # 戻り値の型ヒントを追加
                node.returns = ast.parse(return_type).body[0].value
        return ast.unparse(tree)

    @staticmethod
    def convert_print_to_logging(source_code: str) -> str:
        """print文をロギングに変換"""
        tree = ast.parse(source_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
                # print文をlogging.infoに変換
                node.func = ast.Name(id='logging.info', ctx=ast.Load())
                # 文字列をダブルクォートに統一
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        arg.value = arg.value.replace("'", '"')
        return ast.unparse(tree) 