import unittest
from evolve_chip.core.decorators import evolve, EvolutionGoal
from evolve_chip.constraints.checker import check_output, check_resource_constraints

class TestEvolve(unittest.TestCase):
    def setUp(self):
        self.max_memory = 1024 * 1024  # 1MB
        self.max_runtime = 1.0  # 1秒
    
    def test_output_constraint_violation(self):
        @evolve(
            goals=[EvolutionGoal.READABILITY],
            constraints={'output': 'こんにちは、世界！'}
        )
        def greet():
            print("Hello, World!")
        
        result = check_output(greet, greet.constraints['output'])
        self.assertFalse(result)
    
    def test_memory_constraint_violation(self):
        @evolve(
            goals=[EvolutionGoal.READABILITY],
            constraints={'memory': '< 1MB'}
        )
        def memory_intensive():
            # 大きなリストを生成
            return [i for i in range(1000000)]
        
        result = check_resource_constraints(memory_intensive, memory_intensive.constraints)
        self.assertFalse(result[0])  # メモリ制約違反
    
    def test_runtime_constraint_violation(self):
        @evolve(
            goals=[EvolutionGoal.READABILITY],
            constraints={'runtime': '< 0.1s'}
        )
        def slow_function():
            import time
            time.sleep(0.2)  # 0.2秒待機
            return 42
        
        result = check_resource_constraints(slow_function, slow_function.constraints)
        self.assertFalse(result[1])  # 実行時間制約違反
    
    def test_multiple_constraint_violations(self):
        @evolve(
            goals=[EvolutionGoal.READABILITY],
            constraints={
                'output': 'こんにちは、世界！',
                'memory': '< 1MB',
                'runtime': '< 0.1s'
            }
        )
        def problematic_function():
            import time
            time.sleep(0.2)  # 0.2秒待機
            print("Hello, World!")
            return [i for i in range(1000000)]  # メモリ使用量大
        
        output_ok = check_output(problematic_function, problematic_function.constraints['output'])
        self.assertFalse(output_ok)
        
        memory_ok, runtime_ok = check_resource_constraints(problematic_function, problematic_function.constraints)
        self.assertFalse(memory_ok)
        self.assertFalse(runtime_ok)

if __name__ == '__main__':
    unittest.main() 