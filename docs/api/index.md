# API リファレンス

このセクションでは、EvolveChipの各クラスやメソッドの詳細な説明を提供します。

## 目次

- [evolve デコレータ](./evolve.md)
- [EvolutionGoal](./evolution_goal.md)
- [EvolutionSuggestion](./evolution_suggestion.md)
- [AIEngine](./ai_engine.md)
- [ASTAnalyzer](./ast_analyzer.md)
- [CodeTransformer](./code_transformer.md)

## パッケージ構造

EvolveChipは以下のようなパッケージ構造を持っています：

```
evolve_chip/
├── __init__.py
├── cli.py                # コマンドラインインターフェース
├── core/                 # コア機能
│   ├── __init__.py
│   ├── decorator.py      # evolveデコレータの実装
│   └── chip.py           # EvolveChipクラスの実装
├── models/               # データモデル
│   ├── __init__.py
│   ├── goal.py           # EvolutionGoalの定義
│   └── suggestion.py     # EvolutionSuggestionの定義
├── ai/                   # AI関連機能
│   ├── __init__.py
│   ├── engine.py         # AIEngineインターフェースと実装
│   └── client.py         # Gemini APIクライアント
└── transform/            # コード変換機能
    ├── __init__.py
    └── ast.py            # ASTベースの解析と変換
```

## 主要なクラスと関数

### evolve デコレータ

```python
from evolve_chip import evolve

@evolve(
    goals=[...],
    constraints=[...],
    ai_engine=...,
    instructions=...
)
def my_function():
    pass
```

詳細は [evolve デコレータ](./evolve.md) を参照してください。

### EvolutionGoal

コード進化の目標を表す列挙型です。

```python
from evolve_chip import EvolutionGoal

goals = [
    EvolutionGoal.READABILITY,
    EvolutionGoal.PERFORMANCE
]
```

詳細は [EvolutionGoal](./evolution_goal.md) を参照してください。

### AIEngine

AI分析エンジンのインターフェースと実装です。

```python
from evolve_chip import DefaultAIEngine

ai_engine = DefaultAIEngine()
```

カスタムエンジンを作成することも可能です。

```python
from evolve_chip import AIEngine

class CustomAIEngine(AIEngine):
    def analyze(self, code, goals, constraints=None):
        # カスタム分析ロジック
        return []
        
    def analyze_with_instructions(self, code, instructions, goals, constraints=None):
        # 指示に基づく分析ロジック
        return []
```

詳細は [AIEngine](./ai_engine.md) を参照してください。

## 詳細情報

各クラスやメソッドの詳細な情報については、それぞれのページを参照してください。 