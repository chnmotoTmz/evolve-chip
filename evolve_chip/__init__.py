"""
EvolveChip - AIチップを埋め込むためのPythonライブラリ
"""

from .core.decorator import evolve
from .core.chip import EvolutionGoal, EvolutionSuggestion
from .ai.engine import AIEngine, DefaultAIEngine

__version__ = "0.1.0"
__all__ = ["evolve", "EvolutionGoal", "EvolutionSuggestion", "AIEngine", "DefaultAIEngine"]

# CLIエントリポイント
def main():
    from .cli import main as cli_main
    return cli_main()

if __name__ == "__main__":
    main()
