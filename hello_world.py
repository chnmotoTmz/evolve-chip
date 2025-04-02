import os
import logging
from dotenv import load_dotenv
from evolve_chip import evolve, EvolutionGoal, DefaultAIEngine

# .envファイルを読み込む
load_dotenv()

# 開発モードを設定（先に設定する）
os.environ["EVOLVE_MODE"] = "development"

# ロギングを設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("hello_world")

# 設定を確認
logger.debug(f"GEMINI_API_KEY1: {'*****' if os.getenv('GEMINI_API_KEY1') else 'Not set'}")

ai_engine = DefaultAIEngine()
logger.debug(f"AIエンジン作成: {ai_engine.__class__.__name__}")

@evolve(goals=[EvolutionGoal.READABILITY, EvolutionGoal.PERFORMANCE], ai_engine=ai_engine)
def say_hello(name: str = "World") -> None:
    print(f"Hello, {name}!")

if __name__ == "__main__":
    logger.debug("プログラム開始")
    logger.debug(f"EVOLVE_MODE: {os.environ.get('EVOLVE_MODE')}")
    
    # 関数を実行
    logger.debug("say_hello関数を呼び出します")
    say_hello("Alice")
    logger.debug("プログラム終了")
