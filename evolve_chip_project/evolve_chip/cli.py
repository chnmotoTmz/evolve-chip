#!/usr/bin/env python
"""
Evolve Chipのコマンドラインインターフェース
"""

import os
import sys
import click
import yaml
from typing import Optional

# アプリケーションルートのパスを設定
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from evolve_chip.core import EvolutionGoal

@click.group()
def cli():
    """Evolve Chip - コード進化チップCLI"""
    pass

@cli.command("import-plan")
@click.argument("plan_file", type=click.Path(exists=True))
@click.option("--output", "-o", help="インポート後のタスク一覧を出力するファイル")
@click.option("--verbose", "-v", is_flag=True, help="詳細情報を表示")
def import_plan(plan_file: str, output: Optional[str], verbose: bool):
    """
    evolution_plan.yamlファイルをインポートし、EvolveChipのタスクとして登録します。
    
    例：evolve-chip import-plan evolution_plan.yaml
    """
    try:
        # YAMLファイルを読み込む
        with open(plan_file, 'r', encoding='utf-8') as f:
            plan_data = yaml.safe_load(f)
            
        if verbose:
            click.echo(f"ファイルを読み込みました: {plan_file}")
        
        # YAMLの構造を検証
        if 'evolution_tasks' not in plan_data:
            click.echo("エラー: 無効な進化計画ファイルです。'evolution_tasks'セクションが見つかりません。", err=True)
            sys.exit(1)
            
        tasks = plan_data.get('evolution_tasks', [])
        
        if not tasks:
            click.echo("警告: タスクが定義されていません。", err=True)
            return
            
        # タスク情報を保存
        config_dir = os.path.join(os.path.expanduser("~"), ".evolve_chip")
        os.makedirs(config_dir, exist_ok=True)
        
        tasks_file = os.path.join(config_dir, "imported_tasks.yaml")
        
        # 既存のタスクがあれば読み込む
        existing_tasks = {}
        if os.path.exists(tasks_file):
            try:
                with open(tasks_file, 'r', encoding='utf-8') as f:
                    existing_tasks = yaml.safe_load(f) or {}
            except Exception as e:
                if verbose:
                    click.echo(f"既存のタスクファイルを読み込めませんでした: {e}", err=True)
                existing_tasks = {}
        
        # 新しいタスクを追加
        imported_tasks = []
        for task in tasks:
            task_id = task.get('id')
            if not task_id:
                continue
                
            # タスク情報を整形
            imported_task = {
                'id': task_id,
                'description': task.get('description', ''),
                'file': task.get('target', {}).get('file', ''),
                'function': task.get('target', {}).get('function', ''),
                'class': task.get('target', {}).get('class', ''),
                'goals': task.get('goals', ['READABILITY']),
                'instructions': task.get('instructions', ''),
                'priority': task.get('priority', 3),
                'enabled': task.get('enabled', True),
                'imported_from': plan_file
            }
            
            imported_tasks.append(imported_task)
            
        # タスクを保存
        existing_tasks['tasks'] = imported_tasks
        
        with open(tasks_file, 'w', encoding='utf-8') as f:
            yaml.dump(existing_tasks, f, sort_keys=False, allow_unicode=True)
            
        task_count = len(imported_tasks)
        click.echo(f"{task_count}個のタスクをインポートしました。")
        
        if output:
            # 出力ファイルにも保存
            with open(output, 'w', encoding='utf-8') as f:
                yaml.dump(existing_tasks, f, sort_keys=False, allow_unicode=True)
            click.echo(f"タスク一覧を{output}に保存しました。")
            
        if verbose:
            # タスク一覧を表示
            click.echo("\nインポートされたタスク:")
            for i, task in enumerate(imported_tasks, 1):
                click.echo(f"{i}. [{task['priority']}] {task['description']}")
                click.echo(f"   ファイル: {task['file']}, 関数: {task['function']}")
                click.echo(f"   指示: {task['instructions'][:50]}..." if len(task['instructions']) > 50 else f"   指示: {task['instructions']}")
                click.echo("")
    
    except Exception as e:
        click.echo(f"エラーが発生しました: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def main():
    """コマンドラインエントリーポイント"""
    cli()

if __name__ == '__main__':
    main() 