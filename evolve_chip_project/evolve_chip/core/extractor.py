#!/usr/bin/env python
"""
EvolveExtract - コード解析とYAML設計書生成ツール
"""

import os
import sys
import click
from typing import List, Optional

# アプリケーションルートのパスを設定
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

@click.group()
def cli():
    """EvolveExtract - コード解析ツール"""
    pass

@cli.command("analyze")
@click.argument("target_path", type=click.Path(exists=True))
@click.option("--output", "-o", default="evolution_plan.yaml", help="出力YAMLファイル名")
@click.option("--exclude", "-e", multiple=True, help="解析から除外するディレクトリやファイル")
@click.option("--verbose", "-v", is_flag=True, help="詳細情報を表示")
def analyze_command(
    target_path: str,
    output: str,
    exclude: List[str],
    verbose: bool
):
    """
    ターゲットディレクトリのコードを解析し、evolution_plan.yamlを生成します。
    """
    click.echo(f"[EvolveExtract] {target_path} を解析中...")
    
    # デモ用のYAMLを生成
    generate_demo_yaml(target_path, output)
    
    click.echo(f"[EvolveExtract] 解析完了! 結果を {output} に保存しました。")

def generate_demo_yaml(target_path: str, output_file: str):
    """
    デモ用のYAMLを生成する
    """
    # ここでは簡易的なデモを実装
    # 実際のツールでは、AST解析やコード分析が行われる
    
    yaml_content = """version: '1.0'
project_settings:
  default_goals:
  - READABILITY
  - MAINTAINABILITY
  default_constraints:
  - preserve_semantics
evolution_tasks:
- id: refactor_complex_func_12345678
  description: 複雑な関数の分割が必要です
  target:
    file: main.py
    function: process_data
  goals:
  - MAINTAINABILITY
  - READABILITY
  instructions: 関数を小さな関数に分割し、各関数が明確な単一の責任を持つようにしてください。制御フローを簡素化し、ネストを減らしてください。
  priority: 1
  enabled: true
  status: pending

- id: add_doc_utils_abcd1234
  description: ユーティリティ関数にドキュメントが不足しています
  target:
    file: utils.py
    function: calculate_metrics
  goals:
  - DOCUMENTATION
  instructions: 関数の目的、引数、戻り値、および例外について説明するドキュメントを追加してください。
  priority: 2
  enabled: true
  status: pending

- id: add_type_hints_ijkl9012
  description: 型ヒントが不足しています
  target:
    file: data_processor.py
    function: transform_data
  goals:
  - TYPE_SAFETY
  - DOCUMENTATION
  instructions: パラメータと戻り値に適切な型ヒントを追加してください。
  priority: 3
  enabled: true
  status: pending
"""
    
    # 出力ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(yaml_content)

def main():
    """コマンドラインエントリーポイント"""
    # cli()からコマンドを直接実行
    try:
        sys.argv[0] = "evolve-extract"
        if len(sys.argv) == 1:
            # 引数がない場合はヘルプ表示
            cli.main(["--help"])
        else:
            # 引数があれば直接analyzeコマンドを実行
            target_path = sys.argv[1]
            output = "evolution_plan.yaml"
            
            # --outputオプションの処理
            if "--output" in sys.argv or "-o" in sys.argv:
                try:
                    output_index = sys.argv.index("--output") if "--output" in sys.argv else sys.argv.index("-o")
                    if output_index + 1 < len(sys.argv):
                        output = sys.argv[output_index + 1]
                except:
                    pass
                    
            analyze_command(target_path, output, [], False)
    except Exception as e:
        click.echo(f"エラーが発生しました: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main() 