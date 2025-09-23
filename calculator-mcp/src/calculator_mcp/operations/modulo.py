"""
取模运算操作
计算一个数除以另一个数的余数
"""
from typing import Type
from pydantic import BaseModel, Field, field_validator
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class ModuloInput(BaseModel):
    """取模运算输入模型"""
    dividend: float = Field(..., description="被除数")
    divisor: float = Field(..., description="除数（模数）")
    
    @field_validator('divisor')
    @classmethod
    def validate_divisor(cls, v):
        if v == 0:
            raise ValueError("除数不能为0")
        return v


class ModuloOperation(BaseOperation):
    """取模运算操作"""
    
    @property
    def name(self) -> str:
        return "modulo"
    
    @property
    def description(self) -> str:
        return "计算取模运算（求余数），a mod b"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return ModuloInput
    
    def validate_input(self, input_data: ModuloInput) -> bool:
        """验证输入数据"""
        return input_data.divisor != 0
    
    async def execute(self, input_data: ModuloInput) -> OperationResult:
        """执行取模运算"""
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                result=0,
                error_message="除数不能为0",
                operation_name=self.name
            )
        
        try:
            # Python的%运算符对负数的处理遵循数学定义
            result = input_data.dividend % input_data.divisor
            
            # 计算商（向下取整）
            quotient = input_data.dividend // input_data.divisor
            
            # 验证：dividend = quotient * divisor + remainder
            verification = quotient * input_data.divisor + result
            
            return OperationResult(
                success=True,
                result=result,
                operation_name=self.name,
                metadata={
                    "dividend": input_data.dividend,
                    "divisor": input_data.divisor,
                    "quotient": quotient,
                    "remainder": result,
                    "notation": f"{input_data.dividend} mod {input_data.divisor}",
                    "equation": f"{input_data.dividend} = {quotient} × {input_data.divisor} + {result}",
                    "verification": verification
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"取模运算失败: {str(e)}",
                operation_name=self.name
            )