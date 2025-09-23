"""
折扣计算操作
计算折扣后价格和折扣金额
"""
from typing import Type
from pydantic import BaseModel, Field
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class DiscountInput(BaseModel):
    original_price: float = Field(..., description="原价", gt=0)
    discount_percent: float = Field(..., description="折扣百分比(如20表示打8折,即20%折扣)", ge=0, le=100)


class DiscountOperation(BaseOperation):
    
    @property
    def name(self) -> str:
        return "discount"
    
    @property
    def description(self) -> str:
        return "计算折扣后价格: 折扣价 = 原价 × (1 - 折扣%/100)"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return DiscountInput
    
    def validate_input(self, input_data: DiscountInput) -> bool:
        if input_data.original_price <= 0:
            return False
        if input_data.discount_percent < 0 or input_data.discount_percent > 100:
            return False
        return True
    
    async def execute(self, input_data: DiscountInput) -> OperationResult:
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                result=0,
                error_message="原价必须大于0, 折扣百分比必须在0-100之间",
                operation_name=self.name
            )
        
        try:
            discount_decimal = input_data.discount_percent / 100
            discount_amount = input_data.original_price * discount_decimal
            final_price = input_data.original_price - discount_amount
            
            savings_percent = input_data.discount_percent
            actual_pay_percent = 100 - input_data.discount_percent
            
            return OperationResult(
                success=True,
                result=final_price,
                operation_name=self.name,
                metadata={
                    "original_price": input_data.original_price,
                    "discount_percent": input_data.discount_percent,
                    "discount_decimal": discount_decimal,
                    "discount_amount": discount_amount,
                    "final_price": final_price,
                    "savings": discount_amount,
                    "savings_percent": savings_percent,
                    "actual_pay_percent": actual_pay_percent,
                    "description": f"原价{input_data.original_price}元, 打{actual_pay_percent}折, 优惠{discount_amount}元"
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"折扣计算失败: {str(e)}",
                operation_name=self.name
            )