# EvolveChip

コードにAIチップを埋め込み、開発時に自己進化をサポートするPythonライブラリ。

## コンセプト

EvolveChipは、コードに「AIチップ」を埋め込み、開発時には自己進化をサポートしながら、本番環境ではその痕跡を完全に取り除くという新しい設計パターンです。

特徴：
- **開発時AI支援**: コードに埋め込まれたAIチップが開発中にコード改善を提案
- **痕跡レス化**: 本番環境ではAIチップを完全に除去
- **モジュール分離**: 環境依存を最小化し、クリーンなコードを保持
- **自然言語による指示**: 「中国語対応にする」など、自然言語による指示でコードを変更

## インストール

```bash
pip install python-dotenv requests
```

## 使用方法

### 基本的な使い方

```python
import os
from evolve_chip import evolve, EvolutionGoal, DefaultAIEngine

# 開発モードを設定
os.environ["EVOLVE_MODE"] = "development"

# AIエンジンの初期化
ai_engine = DefaultAIEngine()

@evolve(goals=[EvolutionGoal.READABILITY, EvolutionGoal.PERFORMANCE], ai_engine=ai_engine)
def say_hello(name: str = "World") -> None:
    print(f"Hello, {name}!")

if __name__ == "__main__":
    say_hello("Alice")
```

### 指示による変更

```python
@evolve(
    goals=[EvolutionGoal.READABILITY],
    ai_engine=ai_engine,
    instructions="このコードをHello, Worldの代わりにHello, Everybodyを表示するように変更してください"
)
def greet_world() -> None:
    print("Hello, World!")
```

### 複雑な指示

```python
@evolve(
    goals=[EvolutionGoal.PERFORMANCE, EvolutionGoal.SECURITY],
    ai_engine=ai_engine,
    instructions="この関数を年齢に応じて挨拶を変えるように改良してください"
)
def age_based_greeting(name: str, age: int) -> None:
    print(f"Hello, {name}!")
```

## 設定

`.env`ファイルを作成し、以下の環境変数を設定します：

```
# Gemini API Keys (1つ以上設定)
GEMINI_API_KEY1=your_gemini_api_key_here

# 開発モード（development/production）
EVOLVE_MODE=development

# ロギング設定
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## 進化目標（EvolutionGoal）

- `READABILITY`: コードの可読性向上
- `PERFORMANCE`: パフォーマンス最適化
- `SECURITY`: セキュリティ強化
- `MAINTAINABILITY`: 保守性向上

## Gemini APIとのインテグレーション

EvolveChipはデフォルトでGemini APIを使用して高度なコード分析と改善提案を行います。
APIキーが設定されていない場合や、API呼び出しに失敗した場合は、ローカル分析にフォールバックします。

## モード切替え

- **開発モード** (`EVOLVE_MODE=development`): AIチップが有効になり、コード改善提案を表示
- **本番モード** (`EVOLVE_MODE`未設定または`production`): AIチップは完全に無効化され、元の関数がそのまま動作

## サンプル

詳しいサンプルは`instructions_example.py`を参照してください。

```bash
python instructions_example.py
```

## 自己進化の例

### 中国語対応の提案

```
指示「このコードを中国語対応にしてください」に基づく分析を実行しました

EvolveChip suggestions for say_hello:
1. 中国語対応:挨拶文の変更 (Priority: 1, Impact: high)
   挨拶文を中国語に変更し、デフォルトの名前も中国語に変更します。また、`name`引数がNoneの場合の処理を追加し、柔軟性を持たせます。
   Example: def say_hello(name: str = '世界') -> None:
    if name is None:
        name = '世界'
    print(f"你好, {name}!")
```

### 年齢別挨拶の提案

```
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
```

## 貢献

バグレポートや機能リクエストは[Issues](https://github.com/yourusername/evolve-chip/issues)で受け付けています。プルリクエストも歓迎します。

## ライセンス

MITライセンス