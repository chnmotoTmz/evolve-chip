"""
汎用AIクライアントの基底クラス定義
"""

import abc
from typing import Dict, Any, Optional, List, Union


class AIClientBase(abc.ABC):
    """
    AIクライアントの基底クラス
    
    様々なAIモデルプロバイダー（OpenAI、Google Gemini、Claude等）の
    共通インターフェースを提供します。
    """
    
    @abc.abstractmethod
    def generate_content(
        self, 
        prompt: str, 
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        テキスト生成を実行する
        
        Args:
            prompt: 入力プロンプト
            options: 生成オプション（温度、トークン数など）
            
        Returns:
            生成結果を含む辞書
        """
        pass
    
    @abc.abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        チャット形式での対話を実行する
        
        Args:
            messages: メッセージリスト（各メッセージは"role"と"content"を含む辞書）
            options: 生成オプション（温度、トークン数など）
            
        Returns:
            生成結果を含む辞書
        """
        pass
        
    @abc.abstractmethod
    def embed(
        self,
        text: Union[str, List[str]],
        options: Optional[Dict[str, Any]] = None
    ) -> List[List[float]]:
        """
        テキストの埋め込みベクトルを取得する
        
        Args:
            text: 埋め込みベクトルを取得するテキスト（または複数テキスト）
            options: 埋め込みオプション
            
        Returns:
            埋め込みベクトルまたはベクトルのリスト
        """
        pass 