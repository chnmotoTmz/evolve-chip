"""
APIキー管理ユーティリティ
"""

import os
import logging
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)


class APIKeyManager:
    """
    APIキーの管理と循環的な使用を提供するクラス
    
    複数のAPIキーを管理し、ローテーションによって
    レート制限の問題を緩和します。
    """
    
    def __init__(
        self, 
        keys: List[str] = None, 
        env_vars: List[str] = None,
        default_env_var: str = None
    ):
        """
        APIキーマネージャーの初期化
        
        Args:
            keys: 直接指定されたAPIキーのリスト
            env_vars: 環境変数名のリスト。指定された環境変数からAPIキーを取得
            default_env_var: デフォルトのAPIキー環境変数名
        """
        self.keys = []
        self.current_index = 0
        
        # 直接指定されたキーを追加
        if keys:
            self.add_keys(keys)
        
        # 環境変数からキーを取得して追加
        if env_vars:
            for env_var in env_vars:
                key = os.environ.get(env_var)
                if key:
                    self.add_key(key)
        
        # デフォルト環境変数からキーを取得
        if default_env_var and not self.keys:
            key = os.environ.get(default_env_var)
            if key:
                self.add_key(key)
    
    def add_key(self, key: str) -> None:
        """単一のAPIキーを追加"""
        if key and key not in self.keys:
            self.keys.append(key)
    
    def add_keys(self, keys: List[str]) -> None:
        """複数のAPIキーを追加"""
        for key in keys:
            self.add_key(key)
    
    def get_key(self) -> Optional[str]:
        """現在のAPIキーを取得"""
        if not self.keys:
            return None
        return self.keys[self.current_index]
    
    def next_key(self) -> Optional[str]:
        """次のAPIキーに移動して取得"""
        if not self.keys:
            return None
            
        self.current_index = (self.current_index + 1) % len(self.keys)
        return self.get_key()
    
    def has_keys(self) -> bool:
        """APIキーが存在するかどうか"""
        return len(self.keys) > 0
    
    def get_key_count(self) -> int:
        """APIキーの数を取得"""
        return len(self.keys) 