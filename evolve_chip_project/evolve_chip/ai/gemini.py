"""
Gemini APIクライアント

Google Gemini APIを利用したAIクライアント実装
"""

import os
import logging
import json
import requests
import random
from typing import Dict, Any, Optional, List, Union
from dotenv import load_dotenv

from .base import AIClientBase
from .models import AIMessage, AIOptions, AIResponse, AIEmbedding

logger = logging.getLogger(__name__)

# .envファイルを読み込み
load_dotenv()

class GeminiClient(AIClientBase):
    """
    Gemini APIクライアント
    
    Google Gemini APIを利用してコード生成を行うクライアント
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Gemini APIクライアントの初期化
        
        Args:
            api_key: Gemini APIキー（未指定時は環境変数から取得）
            
        Raises:
            ValueError: 有効なAPIキーが1つも設定されていない場合
        """
        self.api_keys = []
        self.current_key_index = 0
        
        # 明示的に指定されたキーを追加
        if api_key:
            self.api_keys.append(api_key)
            
        # 環境変数からキーを収集
        env_keys = [
            os.environ.get("GEMINI_API_KEY"),
            os.environ.get("GEMINI_API_KEY1"),
            os.environ.get("GEMINI_API_KEY2")
        ]
        
        # 有効なキーを追加
        for key in env_keys:
            if key and key not in self.api_keys:
                self.api_keys.append(key)
                
        if not self.api_keys:
            raise ValueError("有効なGemini APIキーが設定されていません")
            
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-pro"
        logger.info(f"Gemini APIクライアントを初期化しました（利用可能なキー: {len(self.api_keys)}個）")
    
    def _get_next_api_key(self) -> str:
        """次のAPIキーを取得"""
        key = self.api_keys[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return key
    
    def generate_content(self, prompt: str) -> str:
        """
        プロンプトからコンテンツを生成
        
        Args:
            prompt: 生成のためのプロンプト
            
        Returns:
            生成されたコンテンツ
            
        Raises:
            RuntimeError: すべてのAPIキーでリクエストが失敗した場合
            ValueError: レスポンスに期待されるデータがない場合
        """
        # 全てのキーを試行
        errors = []
        for _ in range(len(self.api_keys)):
            api_key = self._get_next_api_key()
            url = f"{self.base_url}/{self.model}:generateContent"
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": api_key
            }
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
            
            try:
                logger.debug(f"Gemini APIにリクエストを送信: {url}")
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                
                # レスポンスからテキストを抽出
                if "candidates" in result and result["candidates"]:
                    content = result["candidates"][0]["content"]
                    if "parts" in content and content["parts"]:
                        text = content["parts"][0]["text"]
                        logger.debug(f"Gemini APIからの応答: {text[:100]}...")
                        return text
                
                raise ValueError("APIレスポンスに期待されるデータがありません")
                
            except Exception as e:
                logger.warning(f"APIキーでのリクエストに失敗: {str(e)}")
                errors.append(str(e))
                continue
        
        error_msg = f"すべてのAPIキーでリクエストが失敗しました: {'; '.join(errors)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    def chat(self, messages: list) -> str:
        """
        チャット形式でコンテンツを生成
        
        Args:
            messages: メッセージのリスト
            
        Returns:
            生成された応答
        """
        prompt = "\n".join(f"{msg['role']}: {msg['content']}" for msg in messages)
        return self.generate_content(prompt)
    
    def embed(self, text: str) -> list:
        """
        テキストをベクトルに変換
        
        Args:
            text: 変換するテキスト
            
        Returns:
            埋め込みベクトル
        """
        logger.warning("Gemini APIは埋め込み機能を提供していません。モックの結果を返します")
        return [0.0] * 512  # 512次元のゼロベクトル 