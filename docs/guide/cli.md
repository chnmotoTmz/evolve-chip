# コマンドラインツール

EvolveChipは、コマンドラインからも使用できるツールを提供しています。このツールを使用すると、既存のPythonファイルに対してEvolveChipを適用し、コード改善提案を得ることができます。

## 基本的な使い方

インストール後、`evolve-chip`コマンドが利用可能になります。

```bash
# 基本的な使用方法
evolve-chip hello_world.py
```

これにより、指定されたPythonファイルが実行され、ファイル内のevolveデコレータが適用された関数に対して分析が行われます。

## 特定の関数を指定して実行

特定の関数のみを分析したい場合は、`--function`オプションを使用します。

```bash
# 特定の関数を指定して実行
evolve-chip hello_world.py --function say_hello
```

この場合、`say_hello`関数に対してのみAIチップが適用されます。

## 自然言語による指示を与える

AIチップに特定の指示を与えるには、`--instructions`オプションを使用します。

```bash
# 指示付きで実行
evolve-chip hello_world.py --function greet_world --instructions "このコードを中国語対応にしてください"
```

この例では、`greet_world`関数に対して「中国語対応」という指示でAI分析が行われます。

## 複数の進化目標を指定

分析時の進化目標を指定するには、`--goals`オプションを使用します。

```bash
# 複数の進化目標を指定
evolve-chip hello_world.py --function say_hello --goals READABILITY PERFORMANCE SECURITY
```

この例では、可読性、パフォーマンス、セキュリティの3つの目標が指定されています。

## 本番モードでの実行

AIチップを無効化して本番モードで実行するには、`--production`オプションを使用します。

```bash
# 本番モードで実行
evolve-chip hello_world.py --production
```

この場合、AIチップは無効化され、元の関数がそのまま実行されます。

## デコレータ付き関数の一覧表示

ファイル内のevolveデコレータが適用された関数の一覧を表示するには、`--list`オプションを使用します。

```bash
# デコレータ付き関数の一覧表示
evolve-chip hello_world.py --list
```

## 引数を渡して関数を実行

関数に引数を渡して実行するには、`--args`オプションを使用します。

```bash
# 引数を渡して関数を実行
evolve-chip hello_world.py --function say_hello --args "Alice"
```

この例では、`say_hello`関数に"Alice"という引数が渡されます。

## コマンドラインオプション一覧

| オプション | 短縮形 | 説明 |
|------------|--------|------|
| `--function FUNCTION` | `-f FUNCTION` | 特定の関数のみを進化させる場合に指定 |
| `--goals GOALS [GOALS ...]` | `-g GOALS [GOALS ...]` | 進化の目標（READABILITY, PERFORMANCE, SECURITY, MAINTAINABILITY） |
| `--instructions INSTRUCTIONS` | `-i INSTRUCTIONS` | AIに与える自然言語指示 |
| `--production` | `-p` | 本番モードで実行（AIチップを無効化） |
| `--list` | `-l` | 対象ファイル内のevolveデコレータ付き関数を一覧表示 |
| `--args ARGS [ARGS ...]` | `-a ARGS [ARGS ...]` | 関数に渡す引数（スペース区切り） |
| `--help` | `-h` | ヘルプメッセージを表示 |

## ユースケース

### 既存のプロジェクトへの適用

既存のPythonプロジェクトに対してEvolveChipを適用する例：

```bash
# プロジェクト内の特定のファイルに対して実行
evolve-chip src/main.py --function process_data --instructions "この関数をメモリ効率が良くなるように最適化してください"
```

### バッチ処理での活用

シェルスクリプトなどを組み合わせて、複数のファイルに対してバッチ処理を行う例：

```bash
# プロジェクト内の全Pythonファイルに対して実行
for file in $(find . -name "*.py"); do
  evolve-chip $file --list
done
```

## 次のステップ

コマンドラインツールの基本的な使い方を理解したら、[大規模プロジェクトでの活用](./large_projects.md)に進み、より複雑なプロジェクトでの活用方法を学びましょう。 