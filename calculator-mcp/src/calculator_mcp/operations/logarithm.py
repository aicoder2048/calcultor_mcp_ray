"""
对数运算操作
计算自然对数、常用对数或任意底数的对数
"""
import math
from typing import Type
from pydantic import BaseModel, Field, field_validator
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class LogarithmInput(BaseModel):
    """对数运算输入模型"""
    number: float = Field(..., description="被求对数的数字", gt=0)
    base: float = Field(
        math.e, 
        description="对数底数（默认e为自然对数，10为常用对数）", 
        gt=0
    )
    
    @field_validator('base')
    @classmethod
    def validate_base(cls, v):
        if v == 1:
            raise ValueError("对数底数不能为1")
        return v


class LogarithmOperation(BaseOperation):
    """对数运算操作"""
    
    @property
    def name(self) -> str:
        return "logarithm"
    
    @property
    def description(self) -> str:
        return "计算对数值，支持自然对数(ln)、常用对数(log10)和任意底数对数"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return LogarithmInput
    
    def validate_input(self, input_data: LogarithmInput) -> bool:
        """验证输入数据"""
        return input_data.number > 0 and input_data.base > 0 and input_data.base != 1
    
    async def execute(self, input_data: LogarithmInput) -> OperationResult:
        """执行对数运算"""
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                result=0,
                error_message="输入验证失败：数字必须大于0，底数必须大于0且不等于1",
                operation_name=self.name
            )
        
        try:
            if input_data.base == math.e:
                # 自然对数
                result = math.log(input_data.number)
                log_type = "natural"
                notation = f"ln({input_data.number})"
            elif input_data.base == 10:
                # 常用对数
                result = math.log10(input_data.number)
                log_type = "common"
                notation = f"log₁₀({input_data.number})"
            else:
                # 任意底数对数
                result = math.log(input_data.number, input_data.base)
                log_type = "custom"
                notation = f"log_{input_data.base}({input_data.number})"
            
            return OperationResult(
                success=True,
                result=result,
                operation_name=self.name,
                metadata={
                    "number": input_data.number,
                    "base": input_data.base,
                    "log_type": log_type,
                    "notation": notation
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"对数计算失败: {str(e)}",
                operation_name=self.name
            )