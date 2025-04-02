from typing import List, Optional, Any
from ..core.chip import EvolutionSuggestion, EvolutionGoal
from ..transform.ast import ASTAnalyzer, CodeTransformer
from .client import get_ai_client, AIResponse

class AIEngine:
    """AIエンジンの基本クラス"""
    
    def __init__(self, model_name: str = "default"):
        self.model_name = model_name
        self._setup_model()

    def _setup_model(self) -> None:
        """AIモデルのセットアップ"""
        # 実際のAIモデルの初期化処理
        pass

    def analyze(
        self,
        source_code: str,
        goals: List[EvolutionGoal],
        constraints: List[str]
    ) -> List[EvolutionSuggestion]:
        """
        ソースコードを解析し、進化の提案を生成
        
        Args:
            source_code: 解析対象のソースコード
            goals: 進化の目標リスト
            constraints: 制約条件リスト
            
        Returns:
            進化の提案リスト
        """
        # 実際のAI分析ロジック
        return []

class DefaultAIEngine(AIEngine):
    """デフォルトのAIエンジン実装"""
    
    def __init__(self):
        super().__init__()
        self.ai_client = get_ai_client()
    
    def analyze(
        self,
        source_code: str,
        goals: List[EvolutionGoal],
        constraints: List[str]
    ) -> List[EvolutionSuggestion]:
        suggestions = []
        analyzer = ASTAnalyzer(source_code)
        
        # AIによる分析
        try:
            ai_response = self.ai_client.analyze_code(
                source_code,
                [goal.value for goal in goals],
                constraints
            )
            
            # AIの提案を変換
            for ai_suggestion in ai_response.suggestions:
                suggestions.append(
                    EvolutionSuggestion(
                        title=ai_suggestion['title'],
                        description=ai_suggestion['description'],
                        code_sample=ai_suggestion['code'],
                        priority=ai_suggestion['priority'],
                        impact=ai_suggestion['impact']
                    )
                )
        except Exception as e:
            # AIが失敗した場合はフォールバック
            pass
        
        # 型ヒントの提案を追加（優先度2）
        functions = analyzer.find_function_definitions()
        for func in functions:
            if not func['returns']:
                suggestions.append(
                    EvolutionSuggestion(
                        title="戻り値の型ヒント追加",
                        description=f"関数 {func['name']} に戻り値の型ヒントを追加",
                        code_sample=CodeTransformer.add_type_hints(
                            source_code,
                            func['name'],
                            {arg: 'Any' for arg in func['args']},
                            'None'
                        ),
                        priority=2,
                        impact="medium"
                    )
                )
        
        # print文の提案を追加（優先度1）
        prints = analyzer.find_print_statements()
        if prints:
            suggestions.append(
                EvolutionSuggestion(
                    title="ロギング改善",
                    description="print文をロギングに変更",
                    code_sample=CodeTransformer.convert_print_to_logging(source_code),
                    priority=1,
                    impact="high"
                )
            )
            
        return suggestions 