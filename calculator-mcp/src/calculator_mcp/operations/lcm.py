"""
最小公倍数运算操作
计算两个或多个整数的最小公倍数
"""
import math
from typing import Type, List
from pydantic import BaseModel, Field, field_validator
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class LCMInput(BaseModel):
    """最小公倍数运算输入模型"""
    numbers: List[int] = Field(..., description="整数列表", min_length=2)
    
    @field_validator('numbers')
    @classmethod
    def validate_numbers(cls, v):
        if len(v) < 2:
            raise ValueError("计算最小公倍数至少需要2个整数")
        for num in v:
            if not isinstance(num, int):
                raise ValueError(f"列表中包含非整数元素: {num}")
        # 不能包含0
        if 0 in v:
            raise ValueError("包含0无法计算最小公倍数")
        return v


class LCMOperation(BaseOperation):
    """最小公倍数运算操作"""
    
    @property
    def name(self) -> str:
        return "lcm"
    
    @property
    def description(self) -> str:
        return "计算两个或多个整数的最小公倍数（LCM）"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return LCMInput
    
    def validate_input(self, input_data: LCMInput) -> bool:
        """验证输入数据"""
        if len(input_data.numbers) < 2:
            return False
        # 不能包含0
        if 0 in input_data.numbers:
            return False
        return True
    
    async def execute(self, input_data: LCMInput) -> OperationResult:
        """执行最小公倍数运算"""
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                result=0,
                error_message="输入验证失败：至少需要2个非零整数",
                operation_name=self.name
            )
        
        try:
            # 使用绝对值进行计算
            abs_numbers = [abs(n) for n in input_data.numbers]
            
            # 使用公式：LCM(a,b) = |a*b| / GCD(a,b)
            # 对于多个数，递归计算：LCM(a,b,c) = LCM(LCM(a,b), c)
            result = abs_numbers[0]
            for num in abs_numbers[1:]:
                gcd_val = math.gcd(result, num)
                result = (result * num) // gcd_val
            
            # 计算GCD用于验证
            gcd_result = abs_numbers[0]
            for num in abs_numbers[1:]:
                gcd_result = math.gcd(gcd_result, num)
            
            # 验证LCM和GCD的关系
            # 对于两个数：a * b = GCD(a,b) * LCM(a,b)
            product = 1
            for num in abs_numbers:
                product *= num
            
            return OperationResult(
                success=True,
                result=result,
                operation_name=self.name,
                metadata={
                    "count": len(input_data.numbers),
                    "original_numbers": input_data.numbers,
                    "absolute_numbers": abs_numbers,
                    "gcd": gcd_result,
                    "lcm_notation": f"LCM({', '.join(map(str, input_data.numbers))})",
                    "relationship": f"每个数都是LCM的因子，LCM是每个数的倍数"
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"最小公倍数计算失败: {str(e)}",
                operation_name=self.name
            )