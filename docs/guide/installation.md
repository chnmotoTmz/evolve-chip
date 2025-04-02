# インストール方法

EvolveChipをインストールして、AIチップを活用した開発を始めましょう。

## 必要条件

- Python 3.7以上
- pip (Pythonパッケージマネージャー)
- 必要に応じてGemini APIキー

## ステップ1: パッケージのインストール

### pipを使ったインストール

```bash
pip install evolve-chip
```

### 開発版のインストール（GitHubから）

最新の開発版を使用したい場合は、GitHubリポジトリから直接インストールできます。

```bash
git clone https://github.com/yourusername/evolve-chip.git
cd evolve-chip
pip install -e .
```

## ステップ2: 依存関係の確認

EvolveChipは以下の主要な依存関係を持っています：

- `python-dotenv`: 環境変数管理
- `requests`: API通信用

これらの依存関係は自動的にインストールされますが、問題が発生した場合は手動でインストールすることもできます。

```bash
pip install python-dotenv requests
```

## ステップ3: 環境設定

`.env`ファイルをプロジェクトのルートディレクトリに作成し、必要な環境変数を設定します。

```
# Gemini API Keys (最低1つ設定)
GEMINI_API_KEY1=your_gemini_api_key_here

# 開発モード（development/production）
EVOLVE_MODE=development

# ロギング設定
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

`.env.example`ファイルを参考にしてください。

## ステップ4: インストールの確認

以下のコマンドを実行して、EvolveChipが正しくインストールされたことを確認します。

```bash
# コマンドラインツールのヘルプを表示
evolve-chip --help
```

以下のようなヘルプメッセージが表示されれば、インストールは成功です。

```
usage: evolve-chip [-h] [--function FUNCTION]
                   [--goals {READABILITY,PERFORMANCE,SECURITY,MAINTAINABILITY} [...]]
                   [--instructions INSTRUCTIONS] [--production] [--list] [--args ARGS [...]]
                   file

EvolveChip - AIチップを使ったコード進化ツール

positional arguments:
  file                  実行するPythonファイル

options:
  -h, --help            show this help message and exit
  --function FUNCTION, -f FUNCTION
                        特定の関数のみを進化させる場合に指定
  ...
```

## トラブルシューティング

### インストール時のエラー

1. **依存関係のインストールエラー**: 
   ```
   pip install --upgrade setuptools wheel
   ```
   を実行してから再インストールを試みてください。

2. **パーミッションエラー**:
   ```
   pip install --user evolve-chip
   ```
   を使用してユーザースペースにインストールしてください。

3. **Pythonバージョンの問題**:
   Python 3.7以上を使用していることを確認してください。

### GeminiAPIキーの取得方法

Gemini APIキーが必要な場合は、[Google AI Studio](https://aistudio.google.com/)で取得できます。

## 次のステップ

インストールが完了したら、[基本的な使い方](./basic_usage.md)に進み、EvolveChipの基本機能を学びましょう。 