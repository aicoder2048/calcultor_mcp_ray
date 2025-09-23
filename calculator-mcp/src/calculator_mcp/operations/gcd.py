"""
最大公约数运算操作
计算两个或多个整数的最大公约数
"""
import math
from typing import Type, List
from pydantic import BaseModel, Field, field_validator
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class GCDInput(BaseModel):
    """最大公约数运算输入模型"""
    numbers: List[int] = Field(..., description="整数列表", min_length=2)
    
    @field_validator('numbers')
    @classmethod
    def validate_numbers(cls, v):
        if len(v) < 2:
            raise ValueError("计算最大公约数至少需要2个整数")
        for num in v:
            if not isinstance(num, int):
                raise ValueError(f"列表中包含非整数元素: {num}")
        # 至少有一个非零数
        if all(n == 0 for n in v):
            raise ValueError("不能全部为0")
        return v


class GCDOperation(BaseOperation):
    """最大公约数运算操作"""
    
    @property
    def name(self) -> str:
        return "gcd"
    
    @property
    def description(self) -> str:
        return "计算两个或多个整数的最大公约数（GCD）"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return GCDInput
    
    def validate_input(self, input_data: GCDInput) -> bool:
        """验证输入数据"""
        if len(input_data.numbers) < 2:
            return False
        # 不能全部为0
        if all(n == 0 for n in input_data.numbers):
            return False
        return True
    
    async def execute(self, input_data: GCDInput) -> OperationResult:
        """执行最大公约数运算"""
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                result=0,
                error_message="输入验证失败：至少需要2个整数，且不能全部为0",
                operation_name=self.name
            )
        
        try:
            # 使用绝对值进行计算
            abs_numbers = [abs(n) for n in input_data.numbers]
            
            # 使用Python的math.gcd计算多个数的最大公约数
            # math.gcd只接受两个参数，需要递归计算
            result = abs_numbers[0]
            for num in abs_numbers[1:]:
                result = math.gcd(result, num)
                if result == 1:
                    # 如果已经是1，可以提前结束
                    break
            
            # 判断是否互质
            is_coprime = (result == 1)
            
            # 计算每个数除以GCD的结果（化简后的数）
            reduced_numbers = [n // result for n in abs_numbers] if result != 0 else abs_numbers
            
            return OperationResult(
                success=True,
                result=result,
                operation_name=self.name,
                metadata={
                    "count": len(input_data.numbers),
                    "original_numbers": input_data.numbers,
                    "absolute_numbers": abs_numbers,
                    "is_coprime": is_coprime,
                    "reduced_numbers": reduced_numbers,
                    "gcd_notation": f"GCD({', '.join(map(str, input_data.numbers))})"
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"最大公约数计算失败: {str(e)}",
                operation_name=self.name
            )