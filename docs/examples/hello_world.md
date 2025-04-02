# Hello World 例

ここでは、EvolveChipを使用した最も基本的な例として、Hello Worldプログラムを紹介します。この例を通じて、EvolveChipの基本的な機能と使い方を学びましょう。

## 基本的なHello Worldプログラム

まず、基本的なHello Worldプログラムを作成し、evolveデコレータを適用します。

```python
# hello_world.py
import os
import logging
from dotenv import load_dotenv
from evolve_chip import evolve, EvolutionGoal, DefaultAIEngine

# .envファイルを読み込む
load_dotenv()

# 開発モードを設定
os.environ["EVOLVE_MODE"] = "development"

# ロギングを設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("hello_world")

# AIエンジンの初期化
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
```

## プログラムの解説

1. **環境設定**:
   - `.env`ファイルから環境変数を読み込みます
   - 開発モードを設定します（`EVOLVE_MODE=development`）
   - ロギングを設定します

2. **AIエンジンの初期化**:
   - `DefaultAIEngine`のインスタンスを作成します
   - これは、コード分析と改善提案を生成するためのエンジンです

3. **evolveデコレータの適用**:
   - `@evolve`デコレータを`say_hello`関数に適用します
   - 進化目標として`READABILITY`（可読性）と`PERFORMANCE`（パフォーマンス）を指定します
   - AIエンジンを指定します

4. **関数の実行**:
   - `say_hello("Alice")`を呼び出して、関数を実行します

## 実行結果

プログラムを実行すると、次のような結果が表示されます：

```
DEBUG:hello_world:AIエンジン作成: DefaultAIEngine
DEBUG:hello_world:プログラム開始
DEBUG:hello_world:EVOLVE_MODE: development
DEBUG:hello_world:say_hello関数を呼び出します

EvolveChip suggestions for say_hello:
1. ロギング改善 (Priority: 1, Impact: high)
   print文をロギングに変更
   Example: logging.info(f"Hello, {name}!")

2. 戻り値の型ヒント追加 (Priority: 2, Impact: medium)
   関数に戻り値の型ヒントを追加
   Example: def say_hello(name: str = "World") -> None:

Hello, Alice!
DEBUG:hello_world:プログラム終了
```

AIチップが関数を分析し、次の改善提案を生成しました：

1. `print`文をロギングに変更する提案
2. 戻り値の型ヒントを追加する提案

## コマンドラインからの実行

コマンドラインツールを使用しても、同様の結果を得ることができます：

```bash
evolve-chip hello_world.py --function say_hello
```

これにより、`hello_world.py`ファイル内の`say_hello`関数に対してのみAIチップが適用されます。

## 本番モードでの実行

本番環境では、AIチップを無効化することができます。以下のようにコードを変更するか：

```python
# 本番モードを設定
os.environ["EVOLVE_MODE"] = "production"
```

または、コマンドラインツールを使用する場合は：

```bash
evolve-chip hello_world.py --function say_hello --production
```

本番モードでは、AIチップは無効化され、元の関数がそのまま実行されます。出力は以下のようになります：

```
DEBUG:hello_world:AIエンジン作成: DefaultAIEngine
DEBUG:hello_world:プログラム開始
DEBUG:hello_world:EVOLVE_MODE: production
DEBUG:hello_world:say_hello関数を呼び出します
Hello, Alice!
DEBUG:hello_world:プログラム終了
```

AIチップによる分析と提案は表示されなくなります。

## 次のステップ

この基本的な例を理解したら、次は[指示付きの進化](./instructions.md)の例に進み、自然言語による指示を使用した発展的な使い方を学びましょう。 