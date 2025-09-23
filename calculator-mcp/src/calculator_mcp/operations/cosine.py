"""
余弦函数运算操作
计算角度的余弦值
"""
import math
from typing import Type
from pydantic import BaseModel, Field, field_validator
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class CosineInput(BaseModel):
    angle: float = Field(..., description="角度值")
    unit: str = Field("degree", description="单位: 'degree'(角度) 或 'radian'(弧度)")
    
    @field_validator('unit')
    @classmethod
    def validate_unit(cls, v: str) -> str:
        if v not in ['degree', 'radian']:
            raise ValueError("单位必须是 'degree' 或 'radian'")
        return v


class CosineOperation(BaseOperation):
    
    @property
    def name(self) -> str:
        return "cosine"
    
    @property
    def description(self) -> str:
        return "计算角度的余弦值，支持角度(degree)和弧度(radian)两种单位"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return CosineInput
    
    def validate_input(self, input_data: CosineInput) -> bool:
        if not math.isfinite(input_data.angle):
            return False
        return True
    
    async def execute(self, input_data: CosineInput) -> OperationResult:
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                result=0,
                error_message="角度值必须是有限数值",
                operation_name=self.name
            )
        
        try:
            if input_data.unit == "degree":
                angle_rad = math.radians(input_data.angle)
            else:
                angle_rad = input_data.angle
            
            result = math.cos(angle_rad)
            
            if abs(result) < 1e-10:
                result = 0.0
            
            return OperationResult(
                success=True,
                result=result,
                operation_name=self.name,
                metadata={
                    "angle": input_data.angle,
                    "unit": input_data.unit,
                    "angle_radians": angle_rad,
                    "normalized_angle": input_data.angle % 360 if input_data.unit == "degree" else angle_rad % (2 * math.pi)
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"余弦运算失败: {str(e)}",
                operation_name=self.name
            )