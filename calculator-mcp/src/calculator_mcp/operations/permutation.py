"""
排列运算操作
计算 P(n,r) = n!/(n-r)!
"""
import math
from typing import Type
from pydantic import BaseModel, Field
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class PermutationInput(BaseModel):
    n: int = Field(..., description="总数", ge=0)
    r: int = Field(..., description="选取数", ge=0)


class PermutationOperation(BaseOperation):
    
    @property
    def name(self) -> str:
        return "permutation"
    
    @property
    def description(self) -> str:
        return "计算排列数: P(n,r) = n!/(n-r)!, 从n个元素中选取r个元素的排列数"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return PermutationInput
    
    def validate_input(self, input_data: PermutationInput) -> bool:
        if input_data.n < 0 or input_data.r < 0:
            return False
        if input_data.r > input_data.n:
            return False
        if input_data.n > 170:
            return False
        return True
    
    async def execute(self, input_data: PermutationInput) -> OperationResult:
        if not self.validate_input(input_data):
            if input_data.n < 0 or input_data.r < 0:
                error_msg = "n和r必须是非负整数"
            elif input_data.r > input_data.n:
                error_msg = "选取数r不能大于总数n"
            else:
                error_msg = "数值过大(n > 170), 请使用更小的值"
            
            return OperationResult(
                success=False,
                result=0,
                error_message=error_msg,
                operation_name=self.name
            )
        
        try:
            result = math.perm(input_data.n, input_data.r)
            
            return OperationResult(
                success=True,
                result=float(result),
                operation_name=self.name,
                metadata={
                    "n": input_data.n,
                    "r": input_data.r,
                    "result_integer": result,
                    "formula": f"P({input_data.n},{input_data.r}) = {input_data.n}!/({input_data.n}-{input_data.r})!",
                    "calculation": f"{input_data.n}!/{input_data.n - input_data.r}!" if input_data.r > 0 else "1",
                    "meaning": f"从{input_data.n}个元素中选取{input_data.r}个元素的排列数"
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"排列计算失败: {str(e)}",
                operation_name=self.name
            )