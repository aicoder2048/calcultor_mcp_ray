"""
阶乘运算操作
计算 n! = n × (n-1) × ... × 2 × 1
"""
import math
from typing import Type
from pydantic import BaseModel, Field
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class FactorialInput(BaseModel):
    n: int = Field(..., description="非负整数", ge=0)


class FactorialOperation(BaseOperation):
    
    @property
    def name(self) -> str:
        return "factorial"
    
    @property
    def description(self) -> str:
        return "计算阶乘: n! = n × (n-1) × ... × 2 × 1, 其中0! = 1"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return FactorialInput
    
    def validate_input(self, input_data: FactorialInput) -> bool:
        if input_data.n < 0:
            return False
        if input_data.n > 170:
            return False
        return True
    
    async def execute(self, input_data: FactorialInput) -> OperationResult:
        if not self.validate_input(input_data):
            if input_data.n < 0:
                error_msg = "阶乘只定义在非负整数上"
            else:
                error_msg = "数值过大(n > 170会导致溢出), 请使用更小的值"
            
            return OperationResult(
                success=False,
                result=0,
                error_message=error_msg,
                operation_name=self.name
            )
        
        try:
            result = math.factorial(input_data.n)
            
            result_str = str(result)
            digit_count = len(result_str)
            
            return OperationResult(
                success=True,
                result=float(result),
                operation_name=self.name,
                metadata={
                    "n": input_data.n,
                    "result_integer": result,
                    "digit_count": digit_count,
                    "formula": f"{input_data.n}!" if input_data.n <= 10 else f"{input_data.n}!",
                    "calculation": " × ".join([str(i) for i in range(input_data.n, 0, -1)]) if input_data.n <= 6 else f"{input_data.n} × {input_data.n-1} × ... × 2 × 1"
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"阶乘计算失败: {str(e)}",
                operation_name=self.name
            )