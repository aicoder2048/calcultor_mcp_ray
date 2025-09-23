"""
正切函数运算操作
计算角度的正切值
"""
import math
from typing import Type
from pydantic import BaseModel, Field, field_validator
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class TangentInput(BaseModel):
    angle: float = Field(..., description="角度值")
    unit: str = Field("degree", description="单位: 'degree'(角度) 或 'radian'(弧度)")
    
    @field_validator('unit')
    @classmethod
    def validate_unit(cls, v: str) -> str:
        if v not in ['degree', 'radian']:
            raise ValueError("单位必须是 'degree' 或 'radian'")
        return v


class TangentOperation(BaseOperation):
    
    @property
    def name(self) -> str:
        return "tangent"
    
    @property
    def description(self) -> str:
        return "计算角度的正切值，支持角度(degree)和弧度(radian)两种单位"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return TangentInput
    
    def validate_input(self, input_data: TangentInput) -> bool:
        if not math.isfinite(input_data.angle):
            return False
        
        if input_data.unit == "degree":
            normalized = input_data.angle % 360
            if abs(normalized - 90) < 1e-10 or abs(normalized - 270) < 1e-10:
                return False
        else:
            normalized = input_data.angle % (2 * math.pi)
            if abs(normalized - math.pi/2) < 1e-10 or abs(normalized - 3*math.pi/2) < 1e-10:
                return False
        
        return True
    
    async def execute(self, input_data: TangentInput) -> OperationResult:
        if not self.validate_input(input_data):
            if not math.isfinite(input_data.angle):
                error_msg = "角度值必须是有限数值"
            else:
                error_msg = "正切值在90°和270°(或π/2和3π/2)处无定义"
            
            return OperationResult(
                success=False,
                result=0,
                error_message=error_msg,
                operation_name=self.name
            )
        
        try:
            if input_data.unit == "degree":
                angle_rad = math.radians(input_data.angle)
            else:
                angle_rad = input_data.angle
            
            result = math.tan(angle_rad)
            
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
                error_message=f"正切运算失败: {str(e)}",
                operation_name=self.name
            )