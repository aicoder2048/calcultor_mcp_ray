"""
标准差运算操作
计算样本或总体的标准差
"""
import math
from typing import Type, List
from pydantic import BaseModel, Field, field_validator
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class StandardDeviationInput(BaseModel):
    """标准差运算输入模型"""
    numbers: List[float] = Field(..., description="数字列表", min_length=1)
    is_sample: bool = Field(True, description="是否为样本标准差（True）还是总体标准差（False）")
    
    @field_validator('numbers')
    @classmethod
    def validate_numbers(cls, v):
        if len(v) == 0:
            raise ValueError("数字列表不能为空")
        if len(v) == 1:
            raise ValueError("计算标准差至少需要2个数字")
        return v


class StandardDeviationOperation(BaseOperation):
    """标准差运算操作"""
    
    @property
    def name(self) -> str:
        return "standard_deviation"
    
    @property
    def description(self) -> str:
        return "计算数列的标准差，支持样本标准差和总体标准差"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return StandardDeviationInput
    
    def validate_input(self, input_data: StandardDeviationInput) -> bool:
        """验证输入数据"""
        return len(input_data.numbers) >= 2
    
    async def execute(self, input_data: StandardDeviationInput) -> OperationResult:
        """执行标准差运算"""
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                result=0,
                error_message="计算标准差至少需要2个数字",
                operation_name=self.name
            )
        
        try:
            n = len(input_data.numbers)
            
            # 计算平均值
            mean = sum(input_data.numbers) / n
            
            # 计算方差
            squared_differences = [(x - mean) ** 2 for x in input_data.numbers]
            sum_squared_diff = sum(squared_differences)
            
            # 根据是样本还是总体选择除数
            if input_data.is_sample:
                # 样本标准差：除以 n-1（贝塞尔校正）
                variance = sum_squared_diff / (n - 1)
                std_type = "样本标准差"
                divisor = n - 1
            else:
                # 总体标准差：除以 n
                variance = sum_squared_diff / n
                std_type = "总体标准差"
                divisor = n
            
            # 标准差是方差的平方根
            result = math.sqrt(variance)
            
            # 计算变异系数（标准差相对于平均值的比例）
            coefficient_of_variation = (result / abs(mean) * 100) if mean != 0 else None
            
            return OperationResult(
                success=True,
                result=result,
                operation_name=self.name,
                metadata={
                    "count": n,
                    "mean": mean,
                    "variance": variance,
                    "std_type": std_type,
                    "divisor": divisor,
                    "coefficient_of_variation": coefficient_of_variation,
                    "min": min(input_data.numbers),
                    "max": max(input_data.numbers),
                    "range": max(input_data.numbers) - min(input_data.numbers)
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"标准差计算失败: {str(e)}",
                operation_name=self.name
            )