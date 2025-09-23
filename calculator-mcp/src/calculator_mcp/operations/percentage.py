"""
百分比运算操作
计算百分比、百分比变化率等
"""
from typing import Type, Optional
from pydantic import BaseModel, Field, field_validator
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class PercentageInput(BaseModel):
    """百分比运算输入模型"""
    calculation_type: str = Field(
        "percentage", 
        description="计算类型: percentage(百分比), change(变化率), portion(部分占比), increase(增加百分比), decrease(减少百分比)"
    )
    value: float = Field(..., description="主要值")
    reference: float = Field(..., description="参考值（总数或原始值）")
    
    @field_validator('calculation_type')
    @classmethod
    def validate_calculation_type(cls, v):
        valid_types = ['percentage', 'change', 'portion', 'increase', 'decrease']
        if v not in valid_types:
            raise ValueError(f"计算类型必须是以下之一: {', '.join(valid_types)}")
        return v
    
    @field_validator('reference')
    @classmethod
    def validate_reference(cls, v, info):
        calc_type = info.data.get('calculation_type', 'percentage')
        if calc_type in ['percentage', 'portion', 'change'] and v == 0:
            raise ValueError("参考值不能为0")
        return v


class PercentageOperation(BaseOperation):
    """百分比运算操作"""
    
    @property
    def name(self) -> str:
        return "percentage"
    
    @property
    def description(self) -> str:
        return "计算百分比、变化率、增减百分比等"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return PercentageInput
    
    def validate_input(self, input_data: PercentageInput) -> bool:
        """验证输入数据"""
        if input_data.calculation_type in ['percentage', 'portion', 'change']:
            return input_data.reference != 0
        return True
    
    async def execute(self, input_data: PercentageInput) -> OperationResult:
        """执行百分比运算"""
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                result=0,
                error_message="参考值不能为0",
                operation_name=self.name
            )
        
        try:
            calc_type = input_data.calculation_type
            
            if calc_type == "percentage":
                # 计算value占reference的百分比
                result = (input_data.value / input_data.reference) * 100
                formula = f"({input_data.value} ÷ {input_data.reference}) × 100"
                description = f"{input_data.value} 占 {input_data.reference} 的百分比"
                
            elif calc_type == "change":
                # 计算从reference到value的变化率
                result = ((input_data.value - input_data.reference) / abs(input_data.reference)) * 100
                formula = f"(({input_data.value} - {input_data.reference}) ÷ |{input_data.reference}|) × 100"
                description = f"从 {input_data.reference} 到 {input_data.value} 的变化率"
                
            elif calc_type == "portion":
                # 计算value是reference的多少比例
                result = input_data.value / input_data.reference
                formula = f"{input_data.value} ÷ {input_data.reference}"
                description = f"{input_data.value} 是 {input_data.reference} 的比例"
                
            elif calc_type == "increase":
                # 在reference基础上增加value%
                result = input_data.reference * (1 + input_data.value / 100)
                formula = f"{input_data.reference} × (1 + {input_data.value}/100)"
                description = f"{input_data.reference} 增加 {input_data.value}%"
                
            elif calc_type == "decrease":
                # 在reference基础上减少value%
                result = input_data.reference * (1 - input_data.value / 100)
                formula = f"{input_data.reference} × (1 - {input_data.value}/100)"
                description = f"{input_data.reference} 减少 {input_data.value}%"
            
            return OperationResult(
                success=True,
                result=result,
                operation_name=self.name,
                metadata={
                    "calculation_type": calc_type,
                    "value": input_data.value,
                    "reference": input_data.reference,
                    "formula": formula,
                    "description": description,
                    "unit": "%" if calc_type in ["percentage", "change"] else "ratio"
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"百分比计算失败: {str(e)}",
                operation_name=self.name
            )