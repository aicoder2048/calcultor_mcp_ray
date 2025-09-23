"""
方差运算操作
计算样本或总体的方差
"""
from typing import Type, List
from pydantic import BaseModel, Field, field_validator
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class VarianceInput(BaseModel):
    """方差运算输入模型"""
    numbers: List[float] = Field(..., description="数字列表", min_length=1)
    is_sample: bool = Field(True, description="是否为样本方差（True）还是总体方差（False）")
    
    @field_validator('numbers')
    @classmethod
    def validate_numbers(cls, v):
        if len(v) == 0:
            raise ValueError("数字列表不能为空")
        if len(v) == 1:
            raise ValueError("计算方差至少需要2个数字")
        return v


class VarianceOperation(BaseOperation):
    """方差运算操作"""
    
    @property
    def name(self) -> str:
        return "variance"
    
    @property
    def description(self) -> str:
        return "计算数列的方差，支持样本方差和总体方差"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return VarianceInput
    
    def validate_input(self, input_data: VarianceInput) -> bool:
        """验证输入数据"""
        return len(input_data.numbers) >= 2
    
    async def execute(self, input_data: VarianceInput) -> OperationResult:
        """执行方差运算"""
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                result=0,
                error_message="计算方差至少需要2个数字",
                operation_name=self.name
            )
        
        try:
            n = len(input_data.numbers)
            
            # 计算平均值
            mean = sum(input_data.numbers) / n
            
            # 计算平方差之和
            squared_differences = [(x - mean) ** 2 for x in input_data.numbers]
            sum_squared_diff = sum(squared_differences)
            
            # 根据是样本还是总体选择除数
            if input_data.is_sample:
                # 样本方差：除以 n-1（贝塞尔校正）
                result = sum_squared_diff / (n - 1)
                variance_type = "样本方差"
                divisor = n - 1
            else:
                # 总体方差：除以 n
                result = sum_squared_diff / n
                variance_type = "总体方差"
                divisor = n
            
            # 计算标准差（方差的平方根）
            import math
            standard_deviation = math.sqrt(result)
            
            return OperationResult(
                success=True,
                result=result,
                operation_name=self.name,
                metadata={
                    "count": n,
                    "mean": mean,
                    "variance_type": variance_type,
                    "divisor": divisor,
                    "standard_deviation": standard_deviation,
                    "sum_squared_differences": sum_squared_diff,
                    "min": min(input_data.numbers),
                    "max": max(input_data.numbers),
                    "range": max(input_data.numbers) - min(input_data.numbers)
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"方差计算失败: {str(e)}",
                operation_name=self.name
            )