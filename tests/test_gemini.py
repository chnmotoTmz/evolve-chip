import pytest
import os
from unittest.mock import patch, MagicMock
from evolve_chip.ai.client import AIClient, get_ai_client, APIKeyRotator
from evolve_chip.models.goal import EvolutionGoal
from evolve_chip.models.suggestion import EvolutionSuggestion

# テスト用のサンプルコード
SAMPLE_CODE = """
def hello(name):
    print(f"Hello, {name}!")
    return True
"""

# Gemini APIレスポンスのモック
MOCK_GEMINI_RESPONSE = {
    "candidates": [
        {
            "content": {
                "parts": [
                    {
                        "text": """
以下に改善提案を示します：

[
  {
    "description": "print文をloggingモジュールに置き換えることで、より柔軟なログ出力が可能になります",
    "priority": 1,
    "impact": 0.7,
    "code_example": "import logging\\nlogging.info(f\\"Hello, {name}!\\")"
  },
  {
    "description": "関数のドキュメント文字列（docstring）を追加して、関数の目的と引数を明確にする",
    "priority": 2,
    "impact": 0.5,
    "code_example": "def hello(name):\\n    \\"\\"\\"名前を受け取り挨拶するシンプルな関数\\n    \\n    Args:\\n        name: 挨拶する相手の名前\\n    \\n    Returns:\\n        True: 常に成功を表すTrue値を返す\\n    \\"\\"\\"\\n    print(f\\"Hello, {name}!\\")\\n    return True"
  }
]
"""
                    }
                ]
            }
        }
    ]
}

def test_gemini_api_integration():
    """Gemini API統合のテスト（モック使用）"""
    with patch('evolve_chip.ai.client.GEMINI_API_KEYS', ['dummy_key']), \
         patch('evolve_chip.ai.client.requests.post') as mock_post:
        # APIレスポンスをモック
        mock_response = MagicMock()
        mock_response.json.return_value = MOCK_GEMINI_RESPONSE
        mock_post.return_value = mock_response
        
        # AIクライアントを初期化
        client = AIClient()
        
        # コード分析を実行
        response = client.analyze_code(
            SAMPLE_CODE, 
            [EvolutionGoal.READABILITY, EvolutionGoal.PERFORMANCE]
        )
        
        # APIが呼び出されたことを確認
        mock_post.assert_called_once()
        
        # 結果を検証
        assert len(response.suggestions) == 2
        assert "logging" in response.suggestions[0].description
        assert response.suggestions[0].priority == 1
        assert response.suggestions[1].priority == 2
        assert response.suggestions[0].impact == 0.7
        assert isinstance(response.raw_response, dict)

def test_api_key_rotator():
    """APIキーローテーターのテスト"""
    # 複数のキーでテスト
    rotator = APIKeyRotator(['key1', 'key2', 'key3'])
    assert rotator.get_next_key() == 'key1'
    assert rotator.get_next_key() == 'key2'
    assert rotator.get_next_key() == 'key3'
    assert rotator.get_next_key() == 'key1'  # 循環確認
    
    # 空のキーリストでテスト
    empty_rotator = APIKeyRotator([])
    assert empty_rotator.get_next_key() is None

def test_fallback_with_no_api_key():
    """APIキーがない場合のフォールバックテスト"""
    with patch('evolve_chip.ai.client.GEMINI_API_KEYS', []):
        # AIクライアントを初期化
        client = AIClient()
        
        # コード分析を実行
        response = client.analyze_code(
            SAMPLE_CODE, 
            [EvolutionGoal.READABILITY]
        )
        
        # フォールバックされた結果を検証
        assert len(response.suggestions) > 0
        assert response.raw_response is None

def test_get_ai_client_singleton():
    """AIクライアントのシングルトンパターンのテスト"""
    # シングルトンをリセット
    import evolve_chip.ai.client
    evolve_chip.ai.client._ai_client = None
    
    # 最初の呼び出し
    client1 = get_ai_client()
    
    # 2回目の呼び出し
    client2 = get_ai_client()
    
    # 同じインスタンスであることを確認
    assert client1 is client2 