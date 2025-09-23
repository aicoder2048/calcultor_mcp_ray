"""
幂运算操作
计算 a 的 b 次方
"""
from typing import Type
from pydantic import BaseModel, Field
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class PowerInput(BaseModel):
    """幂运算输入模型"""
    base: float = Field(..., description="底数")
    exponent: float = Field(..., description="指数")


class PowerOperation(BaseOperation):
    """幂运算操作"""
    
    @property
    def name(self) -> str:
        return "power"
    
    @property
    def description(self) -> str:
        return "计算 a 的 b 次方（a^b），支持整数、小数和负数指数"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return PowerInput
    
    def validate_input(self, input_data: PowerInput) -> bool:
        """验证输入数据"""
        # 0的负数次方无定义
        if input_data.base == 0 and input_data.exponent < 0:
            return False
        # 负数的非整数次方可能产生复数
        if input_data.base < 0 and not input_data.exponent.is_integer():
            return False
        return True
    
    async def execute(self, input_data: PowerInput) -> OperationResult:
        """执行幂运算"""
        if not self.validate_input(input_data):
            error_msg = "输入验证失败"
            if input_data.base == 0 and input_data.exponent < 0:
                error_msg = "0的负数次方无定义"
            elif input_data.base < 0 and not input_data.exponent.is_integer():
                error_msg = "负数的非整数次方会产生复数，暂不支持"
            
            return OperationResult(
                success=False,
                result=0,
                error_message=error_msg,
                operation_name=self.name
            )
        
        try:
            result = input_data.base ** input_data.exponent
            
            return OperationResult(
                success=True,
                result=result,
                operation_name=self.name,
                metadata={
                    "base": input_data.base,
                    "exponent": input_data.exponent,
                    "calculation": f"{input_data.base}^{input_data.exponent}"
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"幂运算失败: {str(e)}",
                operation_name=self.name
            )