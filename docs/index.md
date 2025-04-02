# EvolveChip ドキュメント

EvolveChipは、Pythonコードに「AIチップ」を埋め込み、開発時には自己進化をサポートしながら、本番環境ではその痕跡を完全に取り除くという新しい設計パターンを実現するライブラリです。

## 概要

EvolveChipは、開発プロセスをより効率的にする革新的なアプローチを提供します：

- **デコレータベースAPI**: シンプルな`@evolve`デコレータを使用して、任意の関数にAIチップを適用
- **自然言語による指示**: 「このコードを中国語対応にする」などの自然言語指示でコードを変更
- **開発/本番モード切替**: 環境変数一つで開発モードと本番モードを切り替え
- **Gemini API連携**: Google Gemini APIを活用した高度なコード分析と改善提案
- **コマンドラインツール**: CLIから既存のPythonファイルに対してEvolveChipを適用可能

## ドキュメント構成

- [**使用ガイド**](./guide/index.md): インストール方法から基本的な使い方までの説明
- [**API リファレンス**](./api/index.md): クラスやメソッドの詳細な説明
- [**使用例**](./examples/index.md): さまざまなユースケースでの活用例
- [**高度な使用法**](./advanced/index.md): カスタムAIエンジンの作成など高度なトピック

## クイックスタート

### インストール

```bash
pip install evolve-chip
```

### 基本的な使用例

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
    say_hello("Alice")  # AIチップが関数を分析し、改善提案を表示
```

### コマンドラインからの実行

```bash
# 特定の関数を指定して実行
evolve-chip hello_world.py --function say_hello

# 指示付きで実行
evolve-chip hello_world.py --function say_hello --instructions "このコードを中国語対応にしてください"
```

## プロジェクト情報

- **バージョン**: 0.1.0
- **ライセンス**: MIT
- **GitHub**: [https://github.com/yourusername/evolve-chip](https://github.com/yourusername/evolve-chip)
- **作者**: EvolveChip Team 