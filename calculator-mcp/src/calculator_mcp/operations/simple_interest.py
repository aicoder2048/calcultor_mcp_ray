"""
单利计算操作
计算单利利息: I = P × r × t
"""
from typing import Type
from pydantic import BaseModel, Field
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class SimpleInterestInput(BaseModel):
    principal: float = Field(..., description="本金", gt=0)
    rate: float = Field(..., description="年利率(百分比, 如5表示5%)", gt=0)
    time: float = Field(..., description="时间(年)", gt=0)


class SimpleInterestOperation(BaseOperation):
    
    @property
    def name(self) -> str:
        return "simple_interest"
    
    @property
    def description(self) -> str:
        return "计算单利: I = P × r × t, 其中P是本金, r是年利率(%), t是时间(年)"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return SimpleInterestInput
    
    def validate_input(self, input_data: SimpleInterestInput) -> bool:
        if input_data.principal <= 0:
            return False
        if input_data.rate <= 0:
            return False
        if input_data.time <= 0:
            return False
        return True
    
    async def execute(self, input_data: SimpleInterestInput) -> OperationResult:
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                result=0,
                error_message="本金、利率和时间必须都大于0",
                operation_name=self.name
            )
        
        try:
            rate_decimal = input_data.rate / 100
            interest = input_data.principal * rate_decimal * input_data.time
            total_amount = input_data.principal + interest
            
            return OperationResult(
                success=True,
                result=interest,
                operation_name=self.name,
                metadata={
                    "principal": input_data.principal,
                    "rate_percent": input_data.rate,
                    "rate_decimal": rate_decimal,
                    "time_years": input_data.time,
                    "interest": interest,
                    "total_amount": total_amount,
                    "formula": f"{input_data.principal} × {input_data.rate}% × {input_data.time}"
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"单利计算失败: {str(e)}",
                operation_name=self.name
            )