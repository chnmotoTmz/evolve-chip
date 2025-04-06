from evolve_chip.core.decorators import evolve, EvolutionGoal
from evolve_chip.constraints.checker import check_output, check_resource_constraints

@evolve(
    goals=[EvolutionGoal.READABILITY],
    constraints={
        'output': 'Hello World',
        'memory': '< 1MB',
        'runtime': '< 0.1s'
    }
)
def greet():
    print("HW")

@evolve(goals=['readability', 'performance'])
def calculate_fibonacci(n: int) -> int:
    """
    フィボナッチ数列のn番目の数を計算する関数
    
    Args:
        n: 計算するフィボナッチ数列の位置
        
    Returns:
        フィボナッチ数列のn番目の数
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

if __name__ == "__main__":
    greet()
    
    # フィボナッチのテスト
    print(f"Fibonacci(10) = {calculate_fibonacci(10)}") 