"""
中位数运算操作
计算数列的中位数
"""
from typing import Type, List
from pydantic import BaseModel, Field, field_validator
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class MedianInput(BaseModel):
    """中位数运算输入模型"""
    numbers: List[float] = Field(..., description="数字列表", min_length=1)
    
    @field_validator('numbers')
    @classmethod
    def validate_numbers(cls, v):
        if len(v) == 0:
            raise ValueError("数字列表不能为空")
        for num in v:
            if not isinstance(num, (int, float)):
                raise ValueError(f"列表中包含非数字元素: {num}")
        return v


class MedianOperation(BaseOperation):
    """中位数运算操作"""
    
    @property
    def name(self) -> str:
        return "median"
    
    @property
    def description(self) -> str:
        return "计算数列的中位数（中间值）"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return MedianInput
    
    def validate_input(self, input_data: MedianInput) -> bool:
        """验证输入数据"""
        return len(input_data.numbers) > 0
    
    async def execute(self, input_data: MedianInput) -> OperationResult:
        """执行中位数运算"""
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                result=0,
                error_message="数字列表不能为空",
                operation_name=self.name
            )
        
        try:
            # 排序数列
            sorted_numbers = sorted(input_data.numbers)
            n = len(sorted_numbers)
            
            # 计算中位数
            if n % 2 == 1:
                # 奇数个元素，取中间值
                median_index = n // 2
                result = sorted_numbers[median_index]
                calculation_method = "奇数个元素，取中间值"
            else:
                # 偶数个元素，取中间两个数的平均值
                mid_index1 = n // 2 - 1
                mid_index2 = n // 2
                result = (sorted_numbers[mid_index1] + sorted_numbers[mid_index2]) / 2
                calculation_method = "偶数个元素，取中间两个数的平均值"
            
            # 计算四分位数（额外信息）
            q1_index = n // 4
            q3_index = 3 * n // 4
            
            return OperationResult(
                success=True,
                result=result,
                operation_name=self.name,
                metadata={
                    "count": n,
                    "sorted_numbers": sorted_numbers,
                    "calculation_method": calculation_method,
                    "min": sorted_numbers[0],
                    "max": sorted_numbers[-1],
                    "q1_approx": sorted_numbers[q1_index] if n > 1 else result,
                    "q3_approx": sorted_numbers[min(q3_index, n-1)] if n > 1 else result
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"中位数计算失败: {str(e)}",
                operation_name=self.name
            )