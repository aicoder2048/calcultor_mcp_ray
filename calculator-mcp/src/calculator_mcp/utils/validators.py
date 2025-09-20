"""
输入验证工具
提供各种数值验证函数
"""
import math
from typing import Union


def validate_finite_number(value: Union[int, float]) -> bool:
    """验证数值是否为有限数"""
    return not (math.isinf(value) or math.isnan(value))


def validate_non_zero(value: Union[int, float]) -> bool:
    """验证数值是否非零"""
    return value != 0


def validate_non_negative(value: Union[int, float]) -> bool:
    """验证数值是否非负"""
    return value >= 0


def validate_positive(value: Union[int, float]) -> bool:
    """验证数值是否为正数"""
    return value > 0


def validate_integer(value: Union[int, float]) -> bool:
    """验证数值是否为整数"""
    return value == int(value)


def validate_in_range(
    value: Union[int, float], 
    min_val: float = None, 
    max_val: float = None
) -> bool:
    """验证数值是否在指定范围内"""
    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
    return True