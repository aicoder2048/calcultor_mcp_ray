"""
结果格式化工具
处理计算结果的格式化和精度控制
"""
import math
from typing import Union


def format_result(value: Union[int, float], precision: int = 10) -> float:
    """格式化计算结果，处理浮点数精度问题"""
    if isinstance(value, int):
        return float(value)
    
    # 处理特殊值
    if math.isinf(value):
        return value
    if math.isnan(value):
        return value
    
    # 四舍五入到指定精度
    rounded = round(value, precision)
    
    # 如果结果非常接近整数，则返回整数形式
    if abs(rounded - round(rounded)) < 1e-10:
        return float(int(rounded))
    
    return rounded


def format_error_message(operation: str, error: str) -> str:
    """格式化错误消息"""
    return f"[{operation}] {error}"


def is_close_to_integer(value: float, tolerance: float = 1e-10) -> bool:
    """检查浮点数是否接近整数"""
    return abs(value - round(value)) < tolerance