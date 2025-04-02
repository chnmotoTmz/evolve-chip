# EvolveChip - 自己進化型AIチップライブラリ

コードに埋め込むAIチップ技術で、開発時は自動的にコードを進化させ、本番環境では完全に消え去る革新的なフレームワーク。

## 概要

EvolveChipは、開発時にはコードの分析と進化提案を行うAIを「チップ」としてコードに埋め込み、ビルド時には完全に除去することで、両方のメリットを得るアプローチです。

- **開発時**: AI支援によるコード最適化提案
- **本番環境**: 余分なコードなしのクリーンな成果物

## 特徴

- **デコレータベースAPI**: シンプルな`@evolve`デコレータで関数に適用
- **ASTベース解析**: Pythonの抽象構文木を使用した正確なコード解析
- **非侵入的設計**: コアロジックを変更せず、メタデータとして機能
- **自己消滅機能**: ビルド時に完全に除去され、痕跡を残さない
- **環境認識**: 開発モード時のみ動作し、本番環境では自動的に無効化
- **拡張可能なAIエンジン**: カスタムAIエンジンの実装が可能

## インストール

```bash
pip install -e .
```

## 使用方法

### 基本的な使用例

```python
from evolve_chip import evolve, EvolutionGoal, DefaultAIEngine

# カスタムAIエンジンの作成
ai_engine = DefaultAIEngine()

@evolve(
    goals=[EvolutionGoal.READABILITY, EvolutionGoal.PERFORMANCE],
    ai_engine=ai_engine
)
def calculate_sum(a: int, b: int) -> int:
    print(f"Calculating sum of {a} and {b}")
    return a + b

if __name__ == "__main__":
    # 開発モードで実行
    os.environ["EVOLVE_MODE"] = "development"
    result = calculate_sum(5, 3)
    print(f"Result: {result}")
```

### 開発モードでの実行

```bash
# Windowsの場合
set EVOLVE_MODE=development
python your_script.py

# Linux/Macの場合
export EVOLVE_MODE=development
python your_script.py
```

実行すると、AIチップが関数を分析し、以下のような改善提案を表示します：

```
EvolveChip suggestions for calculate_sum:
1. ロギング改善 (Priority: 1, Impact: high)
   print文をロギングに変更
   Example: logging.info(f"Calculating sum of {a} and {b}")

2. 戻り値の型ヒント追加 (Priority: 2, Impact: medium)
   関数 calculate_sum に戻り値の型ヒントを追加
   Example: def calculate_sum(a: int, b: int) -> int:
```

## 主な機能

### 1. ASTベースのコード解析

- 関数定義の解析
- print文の特定
- 型ヒントの分析
- コード構造の理解

### 2. コード変換

- 型ヒントの追加
- print文からロギングへの変換
- コード最適化

### 3. AIエンジン

- デフォルトAIエンジン
- カスタムAIエンジンの実装
- 進化提案の生成

## 開発者向け情報

### カスタムAIエンジンの実装

```python
from evolve_chip import AIEngine, EvolutionSuggestion, EvolutionGoal

class CustomAIEngine(AIEngine):
    def analyze(self, source_code: str, goals: List[EvolutionGoal], constraints: List[str]) -> List[EvolutionSuggestion]:
        # カスタム分析ロジックの実装
        return []
```

### 新しいコード変換の追加

```python
from evolve_chip.transform.ast import CodeTransformer

class CustomTransformer(CodeTransformer):
    @staticmethod
    def custom_transform(source_code: str) -> str:
        # カスタム変換ロジックの実装
        return source_code
```

## 今後の開発予定

1. **複数言語サポート**
   - JavaScript
   - Java
   - C#

2. **高度なAI連携**
   - GPT-4などの大規模言語モデルとの連携
   - コンテキスト認識の向上

3. **IDE統合**
   - VSCode拡張機能
   - JetBrains IDEsプラグイン

4. **ビルドシステム統合**
   - ビルド時のAIチップ除去
   - 最適化パイプライン

## 貢献

バグ報告や機能要望は、Issueで報告してください。Pull Requestも歓迎します。

## ライセンス

MITライセンス #   e v o l v e - c h i p  
 