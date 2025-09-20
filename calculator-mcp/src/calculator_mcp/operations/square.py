"""
平方运算模块
实现数值的平方运算
"""
from typing import Type
from pydantic import BaseModel
from ..base.operation import BaseOperation
from ..base.models import UnaryOperationInput, OperationResult
from ..utils.validators import validate_finite_number
from ..utils.formatters import format_result


class SquareOperation(BaseOperation):
    """平方运算实现"""
    
    @property
    def name(self) -> str:
        return "square"
    
    @property
    def description(self) -> str:
        return "计算平方：返回输入值的平方 (value²)"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return UnaryOperationInput
    
    def validate_input(self, input_data: UnaryOperationInput) -> bool:
        """验证输入数据"""
        return validate_finite_number(input_data.value)
    
    async def execute(self, input_data: UnaryOperationInput) -> OperationResult:
        """执行平方运算"""
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                error_message="输入包含无效数值（无穷大或NaN）",
                operation_name=self.name
            )
        
        try:
            result = input_data.value ** 2
            formatted_result = format_result(result)
            
            return OperationResult(
                success=True,
                result=formatted_result,
                operation_name=self.name
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error_message=f"平方运算失败: {str(e)}",
                operation_name=self.name
            )