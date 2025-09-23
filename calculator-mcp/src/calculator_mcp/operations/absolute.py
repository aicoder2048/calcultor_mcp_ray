"""
绝对值运算操作
返回数值的绝对值
"""
from typing import Type
from pydantic import BaseModel, Field
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class AbsoluteInput(BaseModel):
    """绝对值运算输入模型"""
    number: float = Field(..., description="需要求绝对值的数字")


class AbsoluteOperation(BaseOperation):
    """绝对值运算操作"""
    
    @property
    def name(self) -> str:
        return "absolute"
    
    @property
    def description(self) -> str:
        return "计算数值的绝对值 |x|"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return AbsoluteInput
    
    def validate_input(self, input_data: AbsoluteInput) -> bool:
        """验证输入数据"""
        return True  # 绝对值对所有实数都有定义
    
    async def execute(self, input_data: AbsoluteInput) -> OperationResult:
        """执行绝对值运算"""
        try:
            result = abs(input_data.number)
            
            return OperationResult(
                success=True,
                result=result,
                operation_name=self.name,
                metadata={
                    "original_number": input_data.number,
                    "is_changed": input_data.number < 0,
                    "notation": f"|{input_data.number}|"
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"绝对值计算失败: {str(e)}",
                operation_name=self.name
            )