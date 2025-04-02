#!/usr/bin/env python
import os
import sys
import argparse
import inspect
import importlib.util
from typing import List, Optional, Any

from .core.chip import EvolutionGoal
from .ai.engine import DefaultAIEngine

def load_module_from_file(file_path: str) -> Any:
    """ファイルからモジュールを読み込む"""
    spec = importlib.util.spec_from_file_location("module", file_path)
    if not spec or not spec.loader:
        raise ImportError(f"ファイルを読み込めませんでした: {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def find_functions_with_evolve(module: Any) -> List[str]:
    """モジュール内のevolveデコレータが適用された関数名のリストを取得"""
    functions = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and hasattr(obj, '__wrapped__'):
            functions.append(name)
    return functions

def main():
    parser = argparse.ArgumentParser(description='EvolveChip - AIチップを使ったコード進化ツール')
    parser.add_argument('file', help='実行するPythonファイル')
    parser.add_argument('--function', '-f', help='特定の関数のみを進化させる場合に指定')
    parser.add_argument('--goals', '-g', nargs='+', choices=['READABILITY', 'PERFORMANCE', 'SECURITY', 'MAINTAINABILITY'],
                        default=['READABILITY'], help='進化の目標（複数選択可）')
    parser.add_argument('--instructions', '-i', help='AIに与える自然言語指示（例: "このコードを中国語対応にする"）')
    parser.add_argument('--production', '-p', action='store_true', help='本番モードで実行（AIチップを無効化）')
    parser.add_argument('--list', '-l', action='store_true', help='対象ファイル内のevolveデコレータ付き関数を一覧表示')
    parser.add_argument('--args', '-a', nargs='+', help='関数に渡す引数（スペース区切り）')
    
    args = parser.parse_args()
    
    # モードの設定
    if args.production:
        os.environ["EVOLVE_MODE"] = "production"
    else:
        os.environ["EVOLVE_MODE"] = "development"
    
    # ファイルからモジュールを読み込む
    try:
        module = load_module_from_file(args.file)
    except Exception as e:
        print(f"エラー: {e}")
        return 1
    
    # 関数一覧の表示
    if args.list:
        functions = find_functions_with_evolve(module)
        if functions:
            print(f"ファイル '{args.file}' 内のAIチップ対応関数:")
            for func in functions:
                print(f"  - {func}")
        else:
            print(f"ファイル '{args.file}' 内にAIチップ対応関数はありません")
        return 0
    
    # 指定された関数の実行
    if args.function:
        if not hasattr(module, args.function):
            print(f"エラー: 関数 '{args.function}' はファイル '{args.file}' 内に見つかりません")
            return 1
        
        func = getattr(module, args.function)
        
        # 関数にevolveデコレータを適用（既に適用されている場合は何もしない）
        if not hasattr(func, '__wrapped__'):
            ai_engine = DefaultAIEngine()
            goals = [EvolutionGoal(goal.lower()) for goal in args.goals]
            
            # 元の関数を保存
            original_func = func
            
            # evolveデコレータを動的に適用
            from .core.decorator import evolve
            if args.instructions:
                func = evolve(goals=goals, ai_engine=ai_engine, instructions=args.instructions)(original_func)
            else:
                func = evolve(goals=goals, ai_engine=ai_engine)(original_func)
            
            # モジュールに適用済みの関数を設定
            setattr(module, args.function, func)
        
        # 関数の実行
        function_args = args.args if args.args else []
        result = func(*function_args)
        
        # 結果の表示（必要に応じて）
        if result is not None:
            print(f"\n結果: {result}")
    else:
        # デフォルトでは__main__を実行
        if hasattr(module, '__name__') and module.__name__ == '__main__' and hasattr(module, 'main'):
            module.main()
        else:
            print("警告: ファイルには'main'関数がないか、__name__ == '__main__'ブロックがありません")
            print("--function オプションで特定の関数を指定するか、実行可能なファイルを指定してください")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 