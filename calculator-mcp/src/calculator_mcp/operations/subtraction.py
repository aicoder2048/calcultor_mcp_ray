"""
减法运算模块
实现两个数的减法运算
"""
from typing import Type
from pydantic import BaseModel
from ..base.operation import BaseOperation
from ..base.models import BinaryOperationInput, OperationResult
from ..utils.validators import validate_finite_number
from ..utils.formatters import format_result


class SubtractionOperation(BaseOperation):
    """减法运算实现"""
    
    @property
    def name(self) -> str:
        return "subtract"
    
    @property
    def description(self) -> str:
        return "执行减法运算：返回两个数的差 (a - b)"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return BinaryOperationInput
    
    def validate_input(self, input_data: BinaryOperationInput) -> bool:
        """验证输入数据"""
        return (validate_finite_number(input_data.a) and 
                validate_finite_number(input_data.b))
    
    async def execute(self, input_data: BinaryOperationInput) -> OperationResult:
        """执行减法运算"""
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                error_message="输入包含无效数值（无穷大或NaN）",
                operation_name=self.name
            )
        
        try:
            result = input_data.a - input_data.b
            formatted_result = format_result(result)
            
            return OperationResult(
                success=True,
                result=formatted_result,
                operation_name=self.name
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error_message=f"减法运算失败: {str(e)}",
                operation_name=self.name
            )