"""
N次方根运算模块
实现数值的N次方根运算，包含特殊情况处理
"""
import math
from typing import Type
from pydantic import BaseModel
from ..base.operation import BaseOperation
from ..base.models import NthRootInput, OperationResult
from ..utils.validators import validate_finite_number, validate_non_zero
from ..utils.formatters import format_result


class NthRootOperation(BaseOperation):
    """N次方根运算实现"""
    
    @property
    def name(self) -> str:
        return "nth_root"
    
    @property
    def description(self) -> str:
        return "计算N次方根：返回输入值的N次方根 (value^(1/n))"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return NthRootInput
    
    def validate_input(self, input_data: NthRootInput) -> bool:
        """验证输入数据"""
        return (validate_finite_number(input_data.value) and 
                validate_finite_number(input_data.n) and
                validate_non_zero(input_data.n))
    
    async def execute(self, input_data: NthRootInput) -> OperationResult:
        """执行N次方根运算"""
        if input_data.n == 0:
            return OperationResult(
                success=False,
                error_message="错误：根的次数不能为零",
                operation_name=self.name
            )
        
        # 处理负数的偶数次根
        if input_data.value < 0 and input_data.n % 2 == 0:
            return OperationResult(
                success=False,
                error_message="错误：不能计算负数的偶数次根",
                operation_name=self.name
            )
        
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                error_message="输入包含无效数值",
                operation_name=self.name
            )
        
        try:
            # 处理负数的奇数次根
            if input_data.value < 0 and input_data.n % 2 == 1:
                result = -(-input_data.value) ** (1/input_data.n)
            else:
                result = input_data.value ** (1/input_data.n)
            
            formatted_result = format_result(result)
            
            return OperationResult(
                success=True,
                result=formatted_result,
                operation_name=self.name
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error_message=f"N次方根运算失败: {str(e)}",
                operation_name=self.name
            )