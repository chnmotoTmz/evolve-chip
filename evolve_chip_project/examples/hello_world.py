"""
EvolveChip Hello World サンプル

このサンプルは、シンプルな挨拶関数がどのように進化するかを示します。
"""

import logging
from evolve_chip.core.decorators import evolve
from evolve_chip.core.evolution import EvolutionGoal
from evolve_chip.ai import MockAIClient

# ロギングの設定
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@evolve(
    goals=[EvolutionGoal.READABILITY],
    constraints={
        'output': 'Hello World',
        'memory': '< 1MB'
    }
)
def greet():
    """
    挨拶を表示する関数
    
    この関数は、AIによって可読性の高い実装に進化します。
    現在の実装は最小限で、'HW'という短縮形を使用しています。
    """
    print("HW")  # AIが"Hello World"に進化

def main():
    """サンプルの実行"""
    print("=== 進化前の実行 ===")
    greet()
    
    print("\n=== 進化メタデータ ===")
    print(f"目標: {greet.__evolution__['goals']}")
    print(f"制約: {greet.__evolution__['constraints']}")
    
    print("\n=== 進化の実行 ===")
    evolution = greet.__evolution__['manager']
    evolved_code = evolution.apply_evolution(greet)
    
    if evolved_code:
        print("\n=== 進化後のコード ===")
        print(evolved_code)
    else:
        print("\n進化に失敗しました")

if __name__ == '__main__':
    main() 