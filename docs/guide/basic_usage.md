# 基本的な使い方

EvolveChipの基本的な使い方を学びましょう。EvolveChipは、コードに埋め込むAIチップを利用して、自然な形でコードの進化を促進します。

## evolveデコレータの使用

EvolveChipの中心となる機能は、`@evolve`デコレータです。このデコレータを関数に適用することで、その関数にAIチップが埋め込まれます。

### 基本的な形式

```python
import os
from evolve_chip import evolve, EvolutionGoal, DefaultAIEngine

# 開発モードを設定
os.environ["EVOLVE_MODE"] = "development"

# AIエンジンの初期化
ai_engine = DefaultAIEngine()

@evolve(goals=[EvolutionGoal.READABILITY], ai_engine=ai_engine)
def say_hello(name: str = "World") -> None:
    print(f"Hello, {name}!")

if __name__ == "__main__":
    say_hello("Alice")
```

上記のコードを実行すると、AIチップが関数を分析し、改善提案を表示します。

### evolveデコレータのパラメータ

デコレータには以下のパラメータを設定できます：

- **goals**: 進化の目標（リスト形式）
  - `EvolutionGoal.READABILITY`: 可読性の向上
  - `EvolutionGoal.PERFORMANCE`: パフォーマンスの最適化
  - `EvolutionGoal.SECURITY`: セキュリティの強化
  - `EvolutionGoal.MAINTAINABILITY`: 保守性の向上
- **constraints**: 制約条件（リスト形式、オプション）
- **ai_engine**: AIエンジンのインスタンス
- **instructions**: AIに与える自然言語指示（オプション）

## 指示による制御

EvolveChipの強力な機能の一つに、自然言語による指示があります。これにより、AIチップに特定の方向性での改善を促すことができます。

```python
@evolve(
    goals=[EvolutionGoal.READABILITY],
    ai_engine=ai_engine,
    instructions="このコードを中国語対応にしてください"
)
def say_hello(name: str = "World") -> None:
    print(f"Hello, {name}!")
```

この例では、AIチップに「中国語対応」という指示を与えています。実行すると、中国語対応のための提案が表示されます。

### 指示の例

- **多言語対応**: "このコードを中国語対応にしてください"
- **機能拡張**: "この関数を年齢に応じて挨拶を変えるように改良してください"
- **最適化**: "この関数を大量データに対して最適化してください"
- **セキュリティ**: "この関数のセキュリティを強化してください"

## 開発モードと本番モード

EvolveChipは、開発モードと本番モードを切り替えることができます。

- **開発モード**: AIチップが有効になり、コード改善提案を表示
- **本番モード**: AIチップは完全に無効化され、元の関数がそのまま動作

環境変数`EVOLVE_MODE`で制御します：

```python
# 開発モード
os.environ["EVOLVE_MODE"] = "development"

# 本番モード
os.environ["EVOLVE_MODE"] = "production"
```

または、`.env`ファイルに設定することもできます：

```
EVOLVE_MODE=development
```

## 改善提案の活用

EvolveChipが生成する改善提案は、以下の形式で表示されます：

```
EvolveChip suggestions for say_hello:
1. ロギング改善 (Priority: 1, Impact: high)
   print文をロギングに変更
   Example: logging.info(f"Hello, {name}!")

2. 戻り値の型ヒント追加 (Priority: 2, Impact: medium)
   関数に戻り値の型ヒントを追加
   Example: def say_hello(name: str = "World") -> None:
```

各提案には以下の情報が含まれます：

- **タイトル**: 改善の概要
- **優先度**: 適用すべき順序（数字が小さいほど優先度が高い）
- **影響度**: 改善によるコードへの影響の大きさ
- **説明**: 改善の詳細な説明
- **サンプルコード**: 改善を適用した例

これらの提案を参考に、コードを手動で改善することができます。

## 次のステップ

基本的な使い方を理解したら、[環境設定](./configuration.md)に進み、より詳細な設定方法を学びましょう。 