"""
AI関連のデータモデル定義
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union


@dataclass
class AIMessage:
    """AIとのメッセージ交換用データクラス"""
    
    role: str
    content: str
    
    def to_dict(self) -> Dict[str, str]:
        """辞書形式に変換"""
        return {
            "role": self.role,
            "content": self.content
        }


@dataclass
class AIOptions:
    """AI生成オプション"""
    
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    top_k: Optional[int] = None
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: Optional[List[str]] = None
    extra_options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResponse:
    """AIレスポンスの共通フォーマット"""
    
    text: str
    raw_response: Dict[str, Any]
    model: str
    usage: Optional[Dict[str, int]] = None
    
    @property
    def token_count(self) -> Optional[int]:
        """合計トークン数を取得（使用量情報がある場合）"""
        if self.usage and "total_tokens" in self.usage:
            return self.usage["total_tokens"]
        return None


@dataclass
class AIEmbedding:
    """埋め込みベクトル結果"""
    
    embedding: List[float]
    text: str
    model: str
    raw_response: Optional[Dict[str, Any]] = None 