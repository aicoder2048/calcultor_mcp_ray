"""
Prompt模块导出
导出所有Prompt相关的类和接口
"""
from .base_prompt import BasePrompt
from .multiplication_table import MultiplicationTablePrompt, MultiplicationTableArguments
from .health_metrics import HealthMetricsPrompt, HealthMetricsArguments

__all__ = [
    "BasePrompt",
    "MultiplicationTablePrompt", 
    "MultiplicationTableArguments",
    "HealthMetricsPrompt",
    "HealthMetricsArguments",
]