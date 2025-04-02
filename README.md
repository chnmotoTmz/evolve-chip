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

### コマンドラインからの実行

EvolveChipはコマンドラインツールとしても使用できます。インストール後、以下のコマンドで実行できます：

```bash
# インストール
pip install -e .

# 基本的な使用方法
evolve-chip hello_world.py

# 特定の関数を指定して実行
evolve-chip hello_world.py --function say_hello

# 指示付きで実行
evolve-chip hello_world.py --function greet_world --instructions "このコードを中国語対応にしてください"

# 複数の進化目標を指定
evolve-chip hello_world.py --function say_hello --goals READABILITY PERFORMANCE SECURITY

# AIチップを無効化（本番モード）で実行
evolve-chip hello_world.py --production

# デコレータ付き関数の一覧表示
evolve-chip hello_world.py --list

# 引数を渡して関数を実行
evolve-chip hello_world.py --function say_hello --args "Alice"
```

コマンドラインオプション：

| オプション | 短縮形 | 説明 |
|------------|--------|------|
| `--function` | `-f` | 特定の関数のみを進化させる場合に指定 |
| `--goals` | `-g` | 進化の目標（READABILITY, PERFORMANCE, SECURITY, MAINTAINABILITY） |
| `--instructions` | `-i` | AIに与える自然言語指示 |
| `--production` | `-p` | 本番モードで実行（AIチップを無効化） |
| `--list` | `-l` | 対象ファイル内のevolveデコレータ付き関数を一覧表示 |
| `--args` | `-a` | 関数に渡す引数（スペース区切り） |

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

## 大規模アプリケーション開発での活用

EvolveChipは単一関数だけでなく、大規模なアプリケーション開発においても強力なツールとなります。

### マイクロサービスアーキテクチャ

複数のマイクロサービスで構成されるシステムで、各サービスごとに異なる進化目標を設定できます：

```python
# ユーザー認証サービス
@evolve(
    goals=[EvolutionGoal.SECURITY, EvolutionGoal.PERFORMANCE],
    ai_engine=ai_engine,
    instructions="OAuthプロトコルに対応させ、セキュリティを強化してください"
)
def authenticate_user(credentials):
    # 認証ロジック
    pass

# データ処理サービス
@evolve(
    goals=[EvolutionGoal.PERFORMANCE, EvolutionGoal.MAINTAINABILITY],
    ai_engine=ai_engine,
    instructions="大量データ処理を最適化し、メモリ使用量を削減してください"
)
def process_data(data_batch):
    # データ処理ロジック
    pass
```

### ウェブアプリケーション

FlaskやDjango等のウェブフレームワークと組み合わせて、エンドポイントやビジネスロジックを進化させることができます：

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
@evolve(
    goals=[EvolutionGoal.PERFORMANCE, EvolutionGoal.MAINTAINABILITY],
    ai_engine=ai_engine,
    instructions="ページネーション機能を追加し、大量ユーザーデータに対応してください"
)
def get_users():
    # ユーザー一覧取得ロジック
    return jsonify(users)

@app.route('/api/process', methods=['POST'])
@evolve(
    goals=[EvolutionGoal.SECURITY],
    ai_engine=ai_engine,
    instructions="入力データのバリデーションを強化し、SQLインジェクション対策を実装してください"
)
def process_data():
    data = request.json
    # データ処理ロジック
    return jsonify(result)
```

### 機械学習パイプライン

データ前処理、モデルトレーニング、予測といった機械学習パイプラインの各段階に適用できます：

```python
@evolve(
    goals=[EvolutionGoal.PERFORMANCE],
    ai_engine=ai_engine,
    instructions="並列処理を導入し、大規模データセットでの前処理を高速化してください"
)
def preprocess_data(dataset):
    # データ前処理ロジック
    return processed_data

@evolve(
    goals=[EvolutionGoal.PERFORMANCE, EvolutionGoal.MAINTAINABILITY],
    ai_engine=ai_engine,
    instructions="モデルのハイパーパラメータ調整を自動化し、精度を向上させてください"
)
def train_model(training_data):
    # モデルトレーニングロジック
    return model
```

### 大規模プロジェクトでのメリット

1. **統一的なコード品質**: プロジェクト全体で一貫した品質基準を適用
2. **継続的な改善**: 新機能開発と並行して既存コードも自動的に改善
3. **チーム全体の効率化**: 全開発者がAIのサポートを受けられる
4. **特定領域の専門知識補完**: セキュリティやパフォーマンスなど専門知識が必要な領域をAIがサポート
5. **自己文書化**: 提案内容が実質的なコードドキュメントとして機能

### スケーラビリティ

EvolveChipは数百から数千の関数を持つ大規模プロジェクトでも効率的に動作します。AIリクエストは必要な時だけ行われ、キャッシュやレート制限の仕組みにより、API使用量も最適化されます。

### 実装例: 大規模ECサイト

```python
# 製品検索エンジン
@evolve(
    goals=[EvolutionGoal.PERFORMANCE],
    ai_engine=ai_engine,
    instructions="検索アルゴリズムをベクトル検索ベースに改良し、関連性スコアリングを改善してください"
)
def search_products(query, filters=None):
    # 検索ロジック
    pass

# 推奨エンジン
@evolve(
    goals=[EvolutionGoal.MAINTAINABILITY, EvolutionGoal.PERFORMANCE],
    ai_engine=ai_engine,
    instructions="協調フィルタリングと内容ベースのハイブリッド推奨システムに進化させてください"
)
def recommend_products(user_id, current_product=None):
    # 推奨ロジック
    pass

# 決済処理
@evolve(
    goals=[EvolutionGoal.SECURITY],
    ai_engine=ai_engine,
    instructions="PCI DSS準拠の決済処理に改良し、不正検出機能を追加してください"
)
def process_payment(order_id, payment_details):
    # 決済ロジック
    pass
```

## 貢献

バグレポートや機能リクエストは[Issues](https://github.com/yourusername/evolve-chip/issues)で受け付けています。プルリクエストも歓迎します。

## ライセンス

MITライセンス