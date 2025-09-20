"""
错误处理工具
提供标准化的错误处理和消息格式化
"""
from typing import Dict, Any


class ValidationError(Exception):
    """输入验证错误"""
    pass


class CalculationError(Exception):
    """计算执行错误"""  
    pass


def create_error_response(operation_name: str, error_message: str) -> Dict[str, Any]:
    """创建标准化的错误响应"""
    return {
        "success": False,
        "error_message": error_message,
        "operation_name": operation_name,
        "result": None
    }


def validate_and_format_error(
    operation_name: str,
    validation_func,
    input_value: Any,
    error_message: str
) -> str:
    """验证输入并返回格式化的错误信息"""
    if not validation_func(input_value):
        return f"[{operation_name}] {error_message}"
    return None