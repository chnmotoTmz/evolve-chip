"""
制約チェッカー

関数の制約条件をチェックする機能を提供します。
"""

import io
import time
import psutil
import logging
from typing import Dict, Tuple, Any, Callable
from contextlib import redirect_stdout

logger = logging.getLogger(__name__)

class ResourceMonitor:
    """リソース使用量を監視するクラス"""
    
    def __init__(self):
        """モニタリングの初期化"""
        self.process = psutil.Process()
        self.start_time = None
        self.end_time = None
        self.peak_memory = 0
        self.peak_cpu = 0
        self.output = ""
    
    def __enter__(self):
        """モニタリング開始"""
        self.start_time = time.time()
        self.peak_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        self.peak_cpu = psutil.cpu_percent(interval=None)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """モニタリング終了"""
        self.end_time = time.time()
        current_memory = self.process.memory_info().rss / 1024 / 1024
        current_cpu = psutil.cpu_percent(interval=None)
        self.peak_memory = max(self.peak_memory, current_memory)
        self.peak_cpu = max(self.peak_cpu, current_cpu)
    
    @property
    def runtime(self) -> float:
        """実行時間を取得（秒）"""
        if self.start_time is None or self.end_time is None:
            return 0
        return self.end_time - self.start_time

def parse_constraint(constraint: str) -> Tuple[float, str]:
    """
    制約条件の文字列をパース
    
    Args:
        constraint: 制約条件の文字列（例: "< 1MB", "< 0.1s"）
        
    Returns:
        (値, 単位)のタプル
        
    Raises:
        ValueError: 不正な制約形式の場合
    """
    parts = constraint.strip().split()
    if len(parts) != 2:
        raise ValueError(f"不正な制約形式: {constraint}")
    
    operator, value = parts
    if operator != "<":
        raise ValueError(f"サポートされていない演算子: {operator}")
    
    # 数値部分と単位を分離
    for i, char in enumerate(value):
        if not (char.isdigit() or char == '.'):
            number = float(value[:i])
            unit = value[i:]
            return number, unit
    
    return float(value), ""

def check_output(func: Callable, expected_output: str) -> bool:
    """
    関数の出力が期待値と一致するかチェック
    
    Args:
        func: チェック対象の関数
        expected_output: 期待される出力
        
    Returns:
        出力が一致する場合はTrue
    """
    # 標準出力をキャプチャ
    output = io.StringIO()
    with redirect_stdout(output):
        func()
    actual_output = output.getvalue().strip()
    
    # 出力を比較
    matches = actual_output == expected_output
    if not matches:
        logger.warning(f"出力が一致しません。期待値: '{expected_output}', 実際: '{actual_output}'")
    return matches

def check_resource_constraints(
    func: Callable,
    constraints: Dict[str, str]
) -> Tuple[bool, bool, bool]:
    """
    関数のリソース使用量が制約を満たすかチェック
    
    Args:
        func: チェック対象の関数
        constraints: 制約条件の辞書
        
    Returns:
        (メモリ制約OK, 実行時間制約OK, CPU制約OK)のタプル
    """
    # 制約値をパース
    memory_limit = None
    if 'memory' in constraints:
        memory_value, memory_unit = parse_constraint(constraints['memory'])
        if memory_unit == 'MB':
            memory_limit = memory_value
        else:
            raise ValueError(f"サポートされていないメモリ単位: {memory_unit}")
    
    runtime_limit = None
    if 'runtime' in constraints:
        runtime_value, runtime_unit = parse_constraint(constraints['runtime'])
        if runtime_unit == 's':
            runtime_limit = runtime_value
        else:
            raise ValueError(f"サポートされていない時間単位: {runtime_unit}")
    
    cpu_limit = None
    if 'cpu' in constraints:
        cpu_value, cpu_unit = parse_constraint(constraints['cpu'])
        if cpu_unit == '%':
            cpu_limit = cpu_value
        else:
            raise ValueError(f"サポートされていないCPU単位: {cpu_unit}")
    
    # リソース使用量を計測
    with ResourceMonitor() as monitor:
        func()
    
    # 制約チェック
    memory_ok = True
    if memory_limit is not None:
        memory_ok = monitor.peak_memory < memory_limit
        if not memory_ok:
            logger.warning(f"メモリ制約違反: {monitor.peak_memory:.2f}MB > {memory_limit}MB")
    
    runtime_ok = True
    if runtime_limit is not None:
        runtime_ok = monitor.runtime < runtime_limit
        if not runtime_ok:
            logger.warning(f"実行時間制約違反: {monitor.runtime:.4f}s > {runtime_limit}s")
    
    cpu_ok = True
    if cpu_limit is not None:
        cpu_ok = monitor.peak_cpu < cpu_limit
        if not cpu_ok:
            logger.warning(f"CPU制約違反: {monitor.peak_cpu:.1f}% > {cpu_limit}%")
    
    # 詳細なログ出力
    logger.info(
        f"リソース使用状況:\n"
        f"- メモリ: {monitor.peak_memory:.2f}MB\n"
        f"- 実行時間: {monitor.runtime:.4f}s\n"
        f"- CPU: {monitor.peak_cpu:.1f}%"
    )
    
    return memory_ok, runtime_ok, cpu_ok 