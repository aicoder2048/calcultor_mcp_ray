"""
数据模型定义
定义所有输入输出模型和错误类型
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class BinaryOperationInput(BaseModel):
    """二元运算输入模型"""
    a: float = Field(..., description="第一个操作数")
    b: float = Field(..., description="第二个操作数")


class UnaryOperationInput(BaseModel):
    """一元运算输入模型"""
    value: float = Field(..., description="输入值")


class NthRootInput(BaseModel):
    """N次方根运算输入模型"""
    value: float = Field(..., description="被开方数")
    n: float = Field(2, description="根的次数，默认为2（平方根）")


class AverageInput(BaseModel):
    """平均数运算输入模型"""
    values: List[float] = Field(..., description="数值列表", min_length=1)


class OperationResult(BaseModel):
    """运算结果模型"""
    success: bool = Field(..., description="运算是否成功")
    result: Optional[float] = Field(None, description="运算结果")
    error_message: Optional[str] = Field(None, description="错误信息")
    operation_name: str = Field(..., description="运算名称")


class CalculatorError(Exception):
    """计算器专用异常"""
    def __init__(self, message: str, operation: str = "unknown"):
        self.message = message
        self.operation = operation
        super().__init__(self.message)