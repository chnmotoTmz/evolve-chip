"""
汎用生成AIクライアントライブラリ
"""

from .base import AIClientBase
from .mock import MockAIClient

__version__ = "0.1.0"
__all__ = ['AIClientBase', 'MockAIClient'] 