"""
平方根运算模块
实现数值的平方根运算，包含负数检查
"""
import math
from typing import Type
from pydantic import BaseModel
from ..base.operation import BaseOperation
from ..base.models import UnaryOperationInput, OperationResult
from ..utils.validators import validate_finite_number, validate_non_negative
from ..utils.formatters import format_result


class SquareRootOperation(BaseOperation):
    """平方根运算实现"""
    
    @property
    def name(self) -> str:
        return "square_root"
    
    @property
    def description(self) -> str:
        return "计算平方根：返回输入值的平方根 (√value)"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return UnaryOperationInput
    
    def validate_input(self, input_data: UnaryOperationInput) -> bool:
        """验证输入数据"""
        return (validate_finite_number(input_data.value) and 
                validate_non_negative(input_data.value))
    
    async def execute(self, input_data: UnaryOperationInput) -> OperationResult:
        """执行平方根运算"""
        if input_data.value < 0:
            return OperationResult(
                success=False,
                error_message="错误：不能计算负数的平方根",
                operation_name=self.name
            )
        
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                error_message="输入包含无效数值",
                operation_name=self.name
            )
        
        try:
            result = math.sqrt(input_data.value)
            formatted_result = format_result(result)
            
            return OperationResult(
                success=True,
                result=formatted_result,
                operation_name=self.name
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error_message=f"平方根运算失败: {str(e)}",
                operation_name=self.name
            )