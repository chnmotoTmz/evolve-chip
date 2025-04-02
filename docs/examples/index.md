# 使用例

このセクションでは、EvolveChipの様々な使用例を紹介します。実際のコード例を通して、EvolveChipがどのように活用できるかを学びましょう。

## 基本的な例

- [Hello World](./hello_world.md): 最も基本的なEvolveChipの使用例
- [指示付きの進化](./instructions.md): 自然言語による指示を使用した例
- [複数の進化目標](./multiple_goals.md): 複数の目標を組み合わせた例

## 実践的な使用例

- [Webアプリケーション](./web_app.md): FlaskやDjangoなどのWebフレームワークでの活用例
- [データ処理](./data_processing.md): パンダスやNumPyを使用したデータ処理での活用例
- [機械学習](./machine_learning.md): 機械学習パイプラインにおける活用例

## 特定領域での活用

- [セキュリティ強化](./security.md): セキュリティ関連のコード改善例
- [パフォーマンス最適化](./performance.md): パフォーマンスに焦点を当てた改善例
- [レガシーコード改善](./legacy_code.md): 古いコードベースの改善例

## コマンドラインからの使用例

- [ファイル分析](./cli_file_analysis.md): コマンドラインツールを使用したファイル分析
- [バッチ処理](./cli_batch.md): 複数のファイルや関数への一括適用
- [CI/CDパイプライン統合](./ci_cd.md): 継続的インテグレーションでの活用例

## サンプルコード

以下は、基本的な使用例のサンプルコードです：

```python
import os
from evolve_chip import evolve, EvolutionGoal, DefaultAIEngine

# 開発モードを設定
os.environ["EVOLVE_MODE"] = "development"

# AIエンジンの初期化
ai_engine = DefaultAIEngine()

@evolve(
    goals=[EvolutionGoal.READABILITY, EvolutionGoal.PERFORMANCE],
    ai_engine=ai_engine,
    instructions="このコードを多言語対応にしてください"
)
def greet(name: str = "World") -> None:
    print(f"Hello, {name}!")

if __name__ == "__main__":
    greet("Alice")
```

より詳細な例については、それぞれのページを参照してください。 