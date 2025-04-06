# EvolveChip

コードの自動進化を支援するPythonパッケージ

## 概要

EvolveChipは、AIを活用してPythonコードを自動的に進化させるツールです。従来の開発プロセスでは、コードを書く、テストする、リファクタリングするといった作業をすべて人間が行う必要がありましたが、EvolveChipはAIを活用して、コード自体が「進化」する仕組みを提供します。

### 主な特徴
- **自動的なコード改善**: AIチップがコードを解析し、可読性やパフォーマンスを向上
- **開発者の負担軽減**: 単純なリファクタリングや最適化作業をAIに任せることが可能
- **本番環境での効率性**: 開発時にはAIチップが動作し、本番環境では痕跡を完全に除去

## インストール

```bash
git clone <repo-url>
cd evolve_chip_project
pip install -r requirements.txt
```

## 環境設定

1. `.env`ファイルを作成：
```bash
# プロジェクトのルートディレクトリに.envファイルを作成
touch .env
```

2. APIキーを設定：
```env
# Gemini APIキー（少なくとも1つは必須）
GEMINI_API_KEY=your-first-key-here
GEMINI_API_KEY1=your-second-key-here  # オプション
GEMINI_API_KEY2=your-third-key-here   # オプション

# その他のAPIキー
SERPER_API_KEY=your-serper-key-here   # オプション
```

注意：
- 最低1つのGemini APIキーが必要です
- 複数のキーを設定すると、自動的にローテーションされます
- キーが無効になった場合、自動的に次のキーを試行します

## YAMLによるオーケストレーション

EvolveChipは、YAMLを使った宣言的な設定によるコード進化の管理をサポートします。

### 基本的なYAML設定例

```yaml
functions:
  - name: say_hello
    goals:
      - READABILITY
      - PERFORMANCE
    instructions: "このコードを中国語対応にしてください"
  - name: greet_world
    goals:
      - READABILITY
    instructions: "Hello, Worldの代わりにHello, Everybodyを表示してください"
global:
  ai_engine: DefaultAIEngine
  mode: development
```

### YAMLの利点
1. **コードと設定の分離**: 進化の設定をコード本体から分離
2. **再利用性と一元管理**: 複数のプロジェクトやチームで共有可能
3. **柔軟な制御**: 進化のプロセスを細かく制御可能

## 使用例

### 基本的な使用例

```python
from evolve_chip.core.decorators import evolve, EvolutionGoal

@evolve(
    goals=[EvolutionGoal.READABILITY],
    constraints={
        'output': 'Hello World',
        'memory': '< 1MB',
        'runtime': '< 0.1s'
    }
)
def greet():
    print("HW")  # AIが"Hello World"に進化

if __name__ == "__main__":
    greet()
```

### タスクリマインダーの例

```python
import logging
from evolve_chip import evolve, EvolutionGoal

@evolve(
    goals=[EvolutionGoal.READABILITY, EvolutionGoal.SECURITY],
    constraints={
        'memory': '< 10MB',
        'runtime': '< 1s'
    }
)
def add_task(task: str, due_date: str) -> None:
    print(f"Task added: {task}, Due: {due_date}")

@evolve(
    goals=[EvolutionGoal.PERFORMANCE],
    constraints={
        'memory': '< 5MB'
    }
)
def remind_tasks(tasks: list) -> None:
    for task in tasks:
        print(f"Reminder: {task}")
```

## APIリファレンス

### @evolve デコレータ

コードを進化させるためのデコレータです。

**構文**:
```python
@evolve(goals=[EvolutionGoal], constraints={dict})
```

**引数**:
- `goals`: 進化の目標を指定するリスト
  - `EvolutionGoal.READABILITY`: コードの可読性を向上
  - `EvolutionGoal.PERFORMANCE`: パフォーマンスを改善
  - `EvolutionGoal.SECURITY`: セキュリティを強化
- `constraints`: 制約条件を指定する辞書
  - `output`: 期待される出力（例: `'Hello World'`）
  - `memory`: メモリ使用量の上限（例: `'< 1MB'`）
  - `runtime`: 実行時間の上限（例: `'< 0.1s'`）
  - `cpu`: CPU使用率の上限（例: `'< 50%'`）

### AIエージェント

コードを自動的に進化させるエージェントです。

**構文**:
```python
from evolve_chip import EvolveAgent

agent = EvolveAgent("evolution_plan.yaml")
agent.evolve_code("hello_world.py")
```

## チュートリアル

### 1. プロジェクトのセットアップ

1. リポジトリをクローン:
   ```bash
   git clone <repo-url>
   cd evolve_chip_project
   ```

2. 依存関係をインストール:
   ```bash
   pip install -r requirements.txt
   ```

3. 環境変数の設定:
   ```bash
   # .envファイルを作成
   cp .env.example .env
   
   # .envファイルを編集してAPIキーを設定
   vim .env
   ```

### 2. 最初のコード進化

1. サンプルコードを作成（`examples/hello_world/v1_initial.py`）:
   ```python
   from evolve_chip.core.decorators import evolve, EvolutionGoal

   @evolve(
       goals=[EvolutionGoal.READABILITY],
       constraints={'output': 'Hello World'}
   )
   def greet():
       print("HW")

   if __name__ == "__main__":
       greet()
   ```

2. オーケストレータを実行:
   ```bash
   python evolve_chip/orchestrator.py
   ```

3. 進化後のコード（`examples/hello_world/v2_evolved.py`）を確認

## 制約の詳細

### 出力制約
- **形式**: `'output': '期待される出力'`
- **説明**: 関数の標準出力が指定された文字列と完全に一致する必要があります
- **例**: `'output': 'Hello World'`

### メモリ制約
- **形式**: `'memory': '< 数値MB'`
- **説明**: 関数の実行時のメモリ使用量が指定された値以下である必要があります
- **例**: `'memory': '< 1MB'`

### 実行時間制約
- **形式**: `'runtime': '< 数値s'`
- **説明**: 関数の実行時間が指定された秒数以下である必要があります
- **例**: `'runtime': '< 0.1s'`

### CPU使用率制約
- **形式**: `'cpu': '< 数値%'`
- **説明**: 関数の実行時のCPU使用率が指定された割合以下である必要があります
- **例**: `'cpu': '< 50%'`

## エラーハンドリング

### APIキーのローテーション
- 複数のAPIキーが設定されている場合、自動的にローテーションされます
- あるキーでエラーが発生した場合、自動的に次のキーを試行します
- すべてのキーが失敗した場合のみ、エラーが発生します

### エラーログ
- ログレベルを`DEBUG`に設定することで、詳細なAPIリクエスト/レスポンスを確認できます
- エラー発生時は`error.log`にエラー内容が記録されます

## 依存関係

- Python 3.8以上
- python-dotenv==1.0.0（環境変数管理）
- requests==2.31.0（API通信）
- psutil==5.9.5（リソース監視）

## プロジェクトの未来

EvolveChipは現在も活発に開発が進められており、以下の機能を計画しています：

1. **自動コード適用**: AIの提案を自動的にコードに適用する機能
2. **多言語対応**: Python以外の言語のサポート
3. **クラウドプラットフォーム**: ウェブベースの進化環境の提供

## コミュニティへの参加

EvolveChipはオープンソースプロジェクトとして、コミュニティからの貢献を歓迎します：

1. **Issue報告**: バグや改善提案の報告
2. **プルリクエスト**: 新機能の追加や既存機能の改善
3. **ドキュメント**: ドキュメントの改善や翻訳

## 研究リファレンス

EvolveChipは、以下の研究成果に基づいて開発されています：

### AI駆動コード最適化研究

最近のAI技術の進歩により、レガシーコードの最適化と改善のためのツールが急速に発展しています。主な研究分野：

1. **コードスメル検出**
   - 不適切なパターンの自動検出
   - パフォーマンス最適化のための深層学習モデル
   - インテリジェントなコードレビューシステム

2. **YAMLベースの構成生成**
   - 自然言語からYAMLコードを生成
   - ドメイン固有の評価指標の開発
   - ITインフラストラクチャの自動構成

3. **自動プログラム修復（APR）**
   - パターンベースのパッチング
   - 動的解析によるバグ検出
   - 検索ベースのAPR
   - 進化的アルゴリズムによる最適化

### 最新の技術動向

EvolveChipに関連する最新の技術動向：

1. **事前訓練モデル**
   - 大規模コードデータセットでの事前訓練
   - ドメイン固有タスクへの転移学習
   - 自己教師あり学習手法

2. **説明可能なAI**
   - 透明性の高い推論プロセス
   - デベロッパーフレンドリーな説明
   - インタラクティブなデバッグ支援

3. **マルチモーダルアプローチ**
   - コード、コメント、ドキュメントの統合分析
   - コンテキストを考慮した最適化
   - 複数のデータソースからの学習

### 参考文献

1. Podduturi, S. (2025). "AI-Driven Code Optimization: Leveraging ML to Refactor Legacy Codebases". North American Journal of Engineering Research.
2. Pujar, S. et al. (2023). "Automated Code generation for Information Technology Tasks in YAML through Large Language Models".
3. Anand, A. et al. (2024). "A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation".
4. AlShriaf, A. et al. (2024). "Automated Configuration Synthesis for Machine Learning Models: A git-Based Requirement and Architecture Management System".

## ライセンス

MITライセンスの下で公開されています。

## プロジェクト構造

```
evolve_chip_project/
├── evolve_chip/
│   ├── core/
│   │   ├── __init__.py
│   │   └── decorators.py       # @evolveデコレータの実装
│   ├── constraints/
│   │   ├── __init__.py
│   │   ├── checker.py         # 制約チェックロジック
│   │   └── basic_rules.yml    # 制約のYAML定義（将来用）
│   └── orchestrator.py        # シンプルなオーケストレータ
├── examples/
│   ├── hello_world/
│   │   ├── v1_initial.py     # 初期コード
│   │   └── v2_evolved.py     # 進化後のコード（手動更新用）
├── tests/
│   ├── __init__.py
│   └── test_evolve.py        # 単体テスト
├── README.md                 # プロジェクト概要と使用方法
├── requirements.txt          # 依存関係
└── setup.py                  # パッケージ化用（オプション）
```

## 制約の定義

制約は以下のように定義できます：

```python
@evolve(
    goals=[EvolutionGoal.READABILITY],
    constraints={
        'output': 'Hello World',
        'memory': '< 1MB',
        'runtime': '< 0.1s'
    }
)
def greet():
    print("HW")
```

## テスト

```bash
python -m unittest tests/test_evolve.py
``` 