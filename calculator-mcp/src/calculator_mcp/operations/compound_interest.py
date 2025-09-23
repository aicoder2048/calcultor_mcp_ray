"""
复利计算操作
计算复利本息: A = P(1 + r/n)^(nt)
"""
from typing import Type
from pydantic import BaseModel, Field
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class CompoundInterestInput(BaseModel):
    principal: float = Field(..., description="本金", gt=0)
    rate: float = Field(..., description="年利率(百分比, 如5表示5%)", gt=0)
    time: float = Field(..., description="时间(年)", gt=0)
    frequency: int = Field(1, description="每年复利次数(1=年, 4=季, 12=月, 365=日)", gt=0)


class CompoundInterestOperation(BaseOperation):
    
    @property
    def name(self) -> str:
        return "compound_interest"
    
    @property
    def description(self) -> str:
        return "计算复利: A = P(1 + r/n)^(nt), P=本金, r=年利率(%), t=时间(年), n=每年复利次数"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return CompoundInterestInput
    
    def validate_input(self, input_data: CompoundInterestInput) -> bool:
        if input_data.principal <= 0:
            return False
        if input_data.rate <= 0:
            return False
        if input_data.time <= 0:
            return False
        if input_data.frequency <= 0:
            return False
        return True
    
    async def execute(self, input_data: CompoundInterestInput) -> OperationResult:
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                result=0,
                error_message="本金、利率、时间和复利次数必须都大于0",
                operation_name=self.name
            )
        
        try:
            rate_decimal = input_data.rate / 100
            
            total_amount = input_data.principal * (
                (1 + rate_decimal / input_data.frequency) ** 
                (input_data.frequency * input_data.time)
            )
            
            interest = total_amount - input_data.principal
            
            frequency_map = {
                1: "年",
                4: "季",
                12: "月",
                365: "日"
            }
            frequency_desc = frequency_map.get(input_data.frequency, f"{input_data.frequency}次/年")
            
            return OperationResult(
                success=True,
                result=total_amount,
                operation_name=self.name,
                metadata={
                    "principal": input_data.principal,
                    "rate_percent": input_data.rate,
                    "rate_decimal": rate_decimal,
                    "time_years": input_data.time,
                    "frequency": input_data.frequency,
                    "frequency_description": frequency_desc,
                    "total_amount": total_amount,
                    "interest": interest,
                    "total_periods": input_data.frequency * input_data.time,
                    "formula": f"{input_data.principal} × (1 + {input_data.rate}%/{input_data.frequency})^({input_data.frequency}×{input_data.time})"
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"复利计算失败: {str(e)}",
                operation_name=self.name
            )