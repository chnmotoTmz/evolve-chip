import pytest
from evolve_chip.transform.ast import ASTAnalyzer, CodeTransformer, ASTNodeInfo

def test_ast_analyzer():
    """ASTAnalyzerのテスト"""
    code = """
def test_function(a: int, b: int) -> int:
    print(f"Calculating sum of {a} and {b}")
    return a + b
"""
    analyzer = ASTAnalyzer(code)
    
    # ノード情報のテスト
    assert len(analyzer.node_info) > 0
    assert any(isinstance(info, ASTNodeInfo) for info in analyzer.node_info)
    
    # 関数定義の検出テスト
    functions = analyzer.find_function_definitions()
    assert len(functions) == 1
    assert functions[0]['name'] == 'test_function'
    assert 'a' in functions[0]['args']
    assert 'b' in functions[0]['args']
    assert functions[0]['returns'] == 'int'
    
    # print文の検出テスト
    prints = analyzer.find_print_statements()
    assert len(prints) == 1
    assert 'Calculating sum of {a} and {b}' in prints[0]['args'][0]

def test_code_transformer():
    """CodeTransformerのテスト"""
    # 型ヒント追加のテスト
    code = """
def test_function(a, b):
    return a + b
"""
    transformed = CodeTransformer.add_type_hints(
        code,
        'test_function',
        {'a': 'int', 'b': 'int'},
        'int'
    )
    assert 'def test_function(a: int, b: int) -> int:' in transformed
    
    # print文からロギングへの変換テスト
    code_with_print = """
def test_function():
    print('test')
"""
    transformed = CodeTransformer.convert_print_to_logging(code_with_print)
    assert "logging.info('test')" in transformed 