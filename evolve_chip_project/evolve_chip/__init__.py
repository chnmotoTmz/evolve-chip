"""
Evolve Chip - コードに進化能力を付与するフレームワーク

このパッケージは、Pythonコードに「進化チップ」を埋め込み、
開発時には自己進化をサポートしながら、本番環境では
その痕跡を完全に取り除く設計パターンを実装します。
"""

from .core.chip import evolve, EvolveChip, EvolutionGoal
from .models.suggestion import EvolutionSuggestion

__version__ = "0.1.0"
__all__ = ["evolve", "EvolveChip", "EvolutionGoal", "EvolutionSuggestion"] 