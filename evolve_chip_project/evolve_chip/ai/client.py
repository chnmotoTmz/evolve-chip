"""
AIクライアントを生成するファクトリー関数
"""

import os
import logging
from typing import Optional, List, Dict, Any, Union

from .base import AIClientBase
from .gemini import GeminiClient
# ここに他のAIクライアント実装をインポート
# from .openai import OpenAIClient
# from .claude import ClaudeClient

logger = logging.getLogger(__name__)


def create_ai_client(
    provider: str = None,
    api_key: Optional[str] = None,
    api_keys: Optional[List[str]] = None,
    model: Optional[str] = None,
    **kwargs
) -> AIClientBase:
    """
    適切なAIクライアントを生成するファクトリー関数
    
    Args:
        provider: AIプロバイダー名（"gemini", "openai", "claude" 等）
                  省略時は環境変数から自動判定
        api_key: APIキー（単一）
        api_keys: 複数のAPIキー
        model: 使用するモデル名
        **kwargs: その他のオプション
        
    Returns:
        適切なAIクライアントインスタンス
        
    Raises:
        ValueError: サポートされていないプロバイダーが指定された場合
    """
    # プロバイダーが指定されていない場合は環境変数から自動判定
    if not provider:
        provider = _detect_provider()
    
    provider = provider.lower()
    
    # Gemini
    if provider == "gemini":
        default_model = model or os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
        return GeminiClient(
            api_key=api_key,
            api_keys=api_keys,
            model=default_model,
            **kwargs
        )
    
    # OpenAI（実装は別途必要）
    elif provider == "openai":
        # default_model = model or os.environ.get("OPENAI_MODEL", "gpt-4")
        # return OpenAIClient(
        #     api_key=api_key,
        #     api_keys=api_keys,
        #     model=default_model,
        #     **kwargs
        # )
        raise NotImplementedError("OpenAIクライアントはまだ実装されていません")
    
    # Claude（実装は別途必要）
    elif provider == "claude":
        # default_model = model or os.environ.get("CLAUDE_MODEL", "claude-3-opus")
        # return ClaudeClient(
        #     api_key=api_key,
        #     api_keys=api_keys,
        #     model=default_model,
        #     **kwargs
        # )
        raise NotImplementedError("Claudeクライアントはまだ実装されていません")
    
    # その他
    else:
        raise ValueError(f"サポートされていないAIプロバイダー: {provider}")


def _detect_provider() -> str:
    """
    環境変数からAIプロバイダーを自動検出
    
    Returns:
        検出されたプロバイダー名（デフォルトは "gemini"）
    """
    # 環境変数から優先的に使用するプロバイダーを取得
    provider = os.environ.get("AI_PROVIDER", "").lower()
    if provider in ["gemini", "openai", "claude"]:
        return provider
    
    # APIキーの存在からプロバイダーを推測
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    elif os.environ.get("OPENAI_API_KEY"):
        return "openai"
    elif os.environ.get("ANTHROPIC_API_KEY"):
        return "claude"
    
    # デフォルトはGemini
    return "gemini" 