# 指示付きの進化

EvolveChipの強力な機能の一つに、自然言語による指示があります。この例では、指示を使ってAIチップにコード変更の方向性を伝える方法を説明します。

## 指示付きのプログラム例

以下は、複数の関数に異なる指示を与える例です：

```python
# instructions_example.py
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
```

## 指示の例と説明

このプログラムでは、3つの異なる関数に異なる指示を与えています：

1. **中国語対応**:
   ```python
   instructions="このコードを中国語対応にしてください"
   ```
   この指示は、`say_hello`関数を中国語対応にするようAIチップに促します。

2. **表示メッセージの変更**:
   ```python
   instructions="このコードをHello, Worldの代わりにHello, Everybodyを表示するように変更してください"
   ```
   この指示は、`greet_world`関数の出力メッセージを変更するよう指示しています。

3. **年齢に応じた挨拶の変更**:
   ```python
   instructions="この関数を年齢に応じて挨拶を変えるように改良してください"
   ```
   この指示は、`age_based_greeting`関数をより高度な機能を持つよう改善するよう指示しています。

## 実行結果

プログラムを実行すると、それぞれの関数に対して異なる改善提案が生成されます：

```
INFO:instructions_example:=== 中国語対応の例 ===

指示「このコードを中国語対応にしてください」に基づく分析を実行しました

EvolveChip suggestions for say_hello:
1. 中国語対応:挨拶文の変更 (Priority: 1, Impact: high)
   挨拶文を中国語に変更し、デフォルトの名前も中国語に変更します。また、`name`引数がNoneの場合の処理を追加し、柔軟性を持たせます。
   Example: def say_hello(name: str = '世界') -> None:
    if name is None:
        name = '世界'
    print(f"你好, {name}!")

Hello, Alice!

INFO:instructions_example:
=== メッセージ変更の例 ===

指示「このコードをHello, Worldの代わりにHello, Everybodyを表示するように変更してください」に基づく分析を実行しました

EvolveChip suggestions for greet_world:
1. メッセージ変更 (Priority: 1, Impact: high)
   "Hello, World!"を"Hello, Everybody!"に変更します。
   Example: def greet_world() -> None:
    print("Hello, Everybody!")

Hello, World!

INFO:instructions_example:
=== 年齢別挨拶の例 ===

指示「この関数を年齢に応じて挨拶を変えるように改良してください」に基づく分析を実行しました

EvolveChip suggestions for age_based_greeting:
1. 年齢に応じた挨拶の変更 (Priority: 1, Impact: high)
   年齢に基づいて挨拶を変えるように関数を修正しました。18歳未満の場合は子供向けの挨拶、60歳以上の場合は丁寧な挨拶、それ以外の場合は一般的な挨拶を使用します。
   Example: def age_based_greeting(name: str, age: int) -> None:
    if age < 0:
        raise ValueError("年齢は0以上の整数である必要があります")
    elif age < 18:
        print(f"こんにちは、{name}ちゃん！")
    elif age >= 60:
        print(f"ご機嫌いかがですか、{name}様。")
    else:
        print(f"こんにちは、{name}さん！")

Hello, Bob!
```

## コマンドラインからの実行

コマンドラインツールを使用しても、同様の結果を得ることができます：

```bash
# 中国語対応の例
evolve-chip instructions_example.py --function say_hello --instructions "このコードを中国語対応にしてください"

# メッセージ変更の例
evolve-chip instructions_example.py --function greet_world --instructions "このコードをHello, Worldの代わりにHello, Everybodyを表示するように変更してください"

# 年齢別挨拶の例
evolve-chip instructions_example.py --function age_based_greeting --instructions "この関数を年齢に応じて挨拶を変えるように改良してください" --args "Bob" 15
```

## 指示の書き方のポイント

効果的な指示を書くためのポイントをいくつか紹介します：

1. **明確さ**: 指示は具体的かつ明確にしましょう
2. **範囲の限定**: 一つの指示で一つの改善に焦点を当てましょう
3. **意図の明示**: 変更の理由や目的を含めると、より適切な提案が得られます
4. **制約の提示**: 必要に応じて制約条件を含めましょう（例：「パフォーマンスを保ちつつ...」）

## 指示のアイデア

以下に、様々な指示のアイデアを示します：

- **多言語対応**: "このコードを多言語対応にしてください"
- **最適化**: "この関数をビッグデータ処理に最適化してください"
- **セキュリティ**: "SQLインジェクション対策を実装してください"
- **エラー処理**: "より堅牢なエラーハンドリングを追加してください"
- **ドキュメント**: "この関数にDocstringを追加してください"
- **テスト**: "この関数のテストケースを生成してください"
- **リファクタリング**: "この関数をより小さな関数に分割してください"

## 次のステップ

指示付きの進化を理解したら、次は[複数の進化目標](./multiple_goals.md)の例に進み、より複雑な目標設定について学びましょう。 