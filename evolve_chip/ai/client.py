import os
import logging
import json
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import requests
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

from ..models.suggestion import EvolutionSuggestion
from ..models.goal import EvolutionGoal

logger = logging.getLogger(__name__)

# ロギングレベルを設定
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format=os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

# Gemini API設定
GEMINI_API_KEYS = [
    os.getenv("GEMINI_API_KEY1", ""),
    os.getenv("GEMINI_API_KEY2", ""),
    os.getenv("GEMINI_API_KEY3", "")
]

# APIキーの存在を確認
for i, key in enumerate(GEMINI_API_KEYS):
    if key:
        logger.debug(f"GEMINI_API_KEY{i+1}が設定されています")

# 最新のGemini API URL
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"

@dataclass
class AIResponse:
    suggestions: List[EvolutionSuggestion]
    raw_response: Optional[Dict[str, Any]] = None

class APIKeyRotator:
    def __init__(self, keys: List[str]):
        self.keys = [k for k in keys if k]  # 空のキーを除外
        self.current_index = 0
        
    def get_next_key(self) -> Optional[str]:
        if not self.keys:
            return None
        key = self.keys[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.keys)
        return key

class AIClient:
    def __init__(self):
        self.key_rotator = APIKeyRotator(GEMINI_API_KEYS)
        
    def analyze_code(
        self,
        code: str,
        goals: List[EvolutionGoal],
        constraints: Optional[List[str]] = None
    ) -> AIResponse:
        api_key = self.key_rotator.get_next_key()
        if not api_key:
            logger.error("No Gemini API key found.")
            raise Exception("Gemini API key not available.")
        
        try:
            prompt = self._build_prompt(code, goals, constraints)
            raw_response = self._call_gemini_api(prompt, api_key)
            suggestions = self._parse_response(raw_response, code)
            
            if not suggestions:
                logger.error("No suggestions from Gemini API.")
                raise Exception("No suggestions from Gemini API.")
                
            return AIResponse(suggestions=suggestions, raw_response=raw_response)
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            raise

    def execute_instructions(
        self,
        code: str,
        instructions: str,
        goals: List[EvolutionGoal],
        constraints: Optional[List[str]] = None
    ) -> AIResponse:
        """指示に基づいてコードを分析・変更する"""
        api_key = self.key_rotator.get_next_key()
        if not api_key:
            logger.error("No Gemini API key found.")
            raise Exception("Gemini API key not available.")
        
        try:
            prompt = self._build_instruction_prompt(code, instructions, goals, constraints)
            raw_response = self._call_gemini_api(prompt, api_key)
            suggestions = self._parse_instruction_response(raw_response, code, instructions)
            
            if not suggestions:
                logger.error("No suggestions from Gemini API for instructions.")
                raise Exception("No suggestions from Gemini API for instructions.")
                
            return AIResponse(suggestions=suggestions, raw_response=raw_response)
        except Exception as e:
            logger.error(f"Error calling Gemini API for instructions: {str(e)}")
            raise
    
    def _build_prompt(
        self,
        code: str,
        goals: List[EvolutionGoal],
        constraints: Optional[List[str]] = None
    ) -> str:
        goals_str = ", ".join([goal.value for goal in goals])
        constraints_str = ", ".join(constraints or [])
        
        return f"""
あなたはPythonコードの品質改善を提案するAIアシスタントです。
以下のコードを分析し、指定された目標に基づいて、改善提案を行ってください。

コード:
```python
{code}
```

目標: {goals_str}
制約: {constraints_str}

以下の形式で回答してください:
[
  {{
    "title": "提案のタイトル",
    "description": "改善提案の詳細な説明",
    "priority": <整数値: 1(高)～5(低)の優先度>,
    "impact": <影響度："high", "medium", "low"のいずれか>,
    "code_example": "改善後のコード例"
  }}
]

少なくとも2つ以上の改善提案をJSON形式で提供してください。
特に、コードの可読性、型安全性、エラーハンドリング、パフォーマンスに注目して分析してください。
"""

    def _call_gemini_api(self, prompt: str, api_key: str) -> Dict[str, Any]:
        url = f"{GEMINI_API_URL}?key={api_key}"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def _parse_response(self, response: Dict[str, Any], original_code: str) -> List[EvolutionSuggestion]:
        try:
            # レスポンスからテキスト部分を抽出
            text = response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            
            # JSONブロックを抽出
            json_start = text.find("[")
            json_end = text.rfind("]") + 1
            
            if json_start == -1 or json_end == 0:
                logger.error("No JSON found in Gemini API response")
                return []
                
            json_text = text[json_start:json_end]
            suggestions_data = json.loads(json_text)
            
            suggestions = []
            for item in suggestions_data:
                suggestions.append(
                    EvolutionSuggestion(
                        title=item.get("title", "AI提案"),
                        description=item.get("description", ""),
                        code_sample=item.get("code_example", ""),
                        priority=item.get("priority", 3),
                        impact=item.get("impact", "medium")
                    )
                )
            
            suggestions.sort(key=lambda x: x.priority)
            return suggestions
        except Exception as e:
            logger.error(f"Error parsing Gemini API response: {str(e)}")
            return []
    
    def _build_instruction_prompt(
        self,
        code: str,
        instructions: str,
        goals: List[EvolutionGoal],
        constraints: Optional[List[str]] = None
    ) -> str:
        goals_str = ", ".join([goal.value for goal in goals])
        constraints_str = ", ".join(constraints or [])
        
        return f"""
あなたはPythonコードを改善・変更するAIアシスタントです。
以下のコードに対して、与えられた指示に基づいて変更を提案してください。

コード:
```python
{code}
```

指示:
{instructions}

目標: {goals_str}
制約: {constraints_str}

以下の形式で回答してください:
[
  {{
    "title": "変更のタイトル",
    "description": "変更内容の詳細な説明",
    "priority": <整数値: 1(高)～5(低)の優先度>,
    "impact": <影響度："high", "medium", "low"のいずれか>,
    "code_example": "変更後のコード例（全体）"
  }}
]

少なくとも1つ以上の変更提案をJSON形式で提供してください。
指示に基づいた変更を行いながら、コードの品質も維持・向上させてください。
"""
    
    def _parse_instruction_response(
        self,
        response: Dict[str, Any],
        original_code: str,
        instructions: str
    ) -> List[EvolutionSuggestion]:
        try:
            # レスポンスからテキスト部分を抽出
            text = response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            
            # JSONブロックを抽出
            json_start = text.find("[")
            json_end = text.rfind("]") + 1
            
            if json_start == -1 or json_end == 0:
                logger.error("No JSON found in Gemini API response")
                return []
                
            json_text = text[json_start:json_end]
            suggestions_data = json.loads(json_text)
            
            suggestions = []
            for item in suggestions_data:
                suggestions.append(
                    EvolutionSuggestion(
                        title=item.get("title", f"指示「{instructions}」に基づく変更"),
                        description=item.get("description", ""),
                        code_sample=item.get("code_example", ""),
                        priority=item.get("priority", 1),
                        impact=item.get("impact", "high")
                    )
                )
            
            suggestions.sort(key=lambda x: x.priority)
            return suggestions
        except Exception as e:
            logger.error(f"Error parsing Gemini API response for instructions: {str(e)}")
            return []
    
# シングルトンインスタンス
_ai_client = None

def get_ai_client() -> AIClient:
    """AIクライアントのシングルトンインスタンスを取得する"""
    global _ai_client
    if _ai_client is None:
        _ai_client = AIClient()
    return _ai_client



