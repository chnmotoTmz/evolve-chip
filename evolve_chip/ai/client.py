import os
import logging
from dataclasses import dataclass
from typing import List, Optional
from dotenv import load_dotenv

from ..models.suggestion import EvolutionSuggestion
from ..models.goal import EvolutionGoal

# 環境変数の読み込み
load_dotenv()

# ロギングの設定
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format=os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger = logging.getLogger(__name__)

@dataclass
class AIResponse:
    """AIの応答を表すデータクラス"""
    suggestions: List[EvolutionSuggestion]
    raw_response: str
    model_name: str
    usage: dict

class AIClient:
    """AIクライアント"""
    
    def __init__(self):
        """AIクライアントの初期化"""
        self.model_name = "local-analyzer"
        logger.info("AIクライアントを初期化しました")
    
    def analyze_code(
        self,
        code: str,
        goals: List[EvolutionGoal],
        constraints: Optional[List[str]] = None
    ) -> AIResponse:
        """コードを分析し、改善提案を生成する"""
        logger.info("コード分析を開始します")
        
        # ローカルな分析のみを行う
        suggestions = []
        
        # 基本的なコード分析
        if "print(" in code:
            suggestions.append(
                EvolutionSuggestion(
                    description="print文をloggingに置き換えることを推奨します",
                    priority=1,
                    impact=0.5,
                    code_example="import logging\nlogging.info('message')"
                )
            )
        
        if "def " in code and "->" not in code:
            suggestions.append(
                EvolutionSuggestion(
                    description="関数に戻り値の型ヒントを追加することを推奨します",
                    priority=2,
                    impact=0.3,
                    code_example="def function() -> str:"
                )
            )
        
        # 応答オブジェクトの作成
        response = AIResponse(
            suggestions=suggestions,
            raw_response="ローカル分析による提案",
            model_name=self.model_name,
            usage={"prompt_tokens": 0, "completion_tokens": 0}
        )
        
        logger.info(f"分析が完了しました。{len(suggestions)}件の提案を生成しました")
        return response
    
    def _build_prompt(
        self,
        code: str,
        goals: List[EvolutionGoal],
        constraints: Optional[List[str]] = None
    ) -> str:
        """プロンプトを構築する（使用しない）"""
        return ""
    
    def _parse_response(self, response: str) -> List[EvolutionSuggestion]:
        """応答を解析する（使用しない）"""
        return []

# シングルトンインスタンス
_ai_client = None

def get_ai_client() -> AIClient:
    """AIクライアントのシングルトンインスタンスを取得する"""
    global _ai_client
    if _ai_client is None:
        _ai_client = AIClient()
    return _ai_client 