import os
import logging
from dotenv import load_dotenv
from evolve_chip import evolve, EvolutionGoal, DefaultAIEngine

# .envファイルを読み込む
load_dotenv()

# 開発モードを設定
os.environ["EVOLVE_MODE"] = "development"

# ロギングを設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("instructions_example")

# AIエンジンの初期化
ai_engine = DefaultAIEngine()

# 指示付きデコレータの使用例
@evolve(
    goals=[EvolutionGoal.READABILITY, EvolutionGoal.PERFORMANCE],
    ai_engine=ai_engine,
    instructions="このコードを中国語対応にしてください"
)
def say_hello(name: str = "World") -> None:
    print(f"Hello, {name}!")

@evolve(
    goals=[EvolutionGoal.READABILITY],
    ai_engine=ai_engine,
    instructions="このコードをHello, Worldの代わりにHello, Everybodyを表示するように変更してください"
)
def greet_world() -> None:
    print("Hello, World!")

@evolve(
    goals=[EvolutionGoal.PERFORMANCE, EvolutionGoal.SECURITY],
    ai_engine=ai_engine,
    instructions="この関数を年齢に応じて挨拶を変えるように改良してください"
)
def age_based_greeting(name: str, age: int) -> None:
    print(f"Hello, {name}!")

if __name__ == "__main__":
    logger.info("=== 中国語対応の例 ===")
    say_hello("Alice")
    
    logger.info("\n=== メッセージ変更の例 ===")
    greet_world()
    
    logger.info("\n=== 年齢別挨拶の例 ===")
    age_based_greeting("Bob", 15) 