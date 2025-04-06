"""
AIクライアントファクトリー

AIクライアントのインスタンスを生成するファクトリー
"""

import os
import logging
from typing import Optional, Dict, Any
from .base import AIClientBase
from .mock import MockAIClient
from .gemini import GeminiClient

logger = logging.getLogger(__name__)

def create_ai_client(
    provider: str = "mock",
    api_key: Optional[str] = None,
    **kwargs
) -> AIClientBase:
    """
    AIクライアントを生成
    
    Args:
        provider: AIプロバイダー名（"mock"または"gemini"）
        api_key: APIキー（オプション）
        **kwargs: その他のオプション
        
    Returns:
        AIClientBaseのインスタンス
        
    Raises:
        ValueError: 不明なプロバイダーが指定された場合
        RuntimeError: Gemini APIキーが設定されていない場合
    """
    # プロバイダーの選択
    if provider == "mock":
        logger.info("Mock AIクライアントを使用します")
        return MockAIClient(**kwargs)
    elif provider == "gemini":
        # APIキーの取得
        api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.warning("Gemini APIキーが設定されていません。Mockクライアントにフォールバックします")
            return MockAIClient(**kwargs)
        
        logger.info("Gemini APIクライアントを使用します")
        return GeminiClient(api_key=api_key)
    else:
        raise ValueError(f"不明なプロバイダー: {provider}") 