"""
平均数运算模块
计算数值列表的算术平均数
"""
from typing import Type
from pydantic import BaseModel
from ..base.operation import BaseOperation
from ..base.models import AverageInput, OperationResult
from ..utils.validators import validate_finite_number
from ..utils.formatters import format_result


class AverageOperation(BaseOperation):
    """平均数运算实现"""
    
    @property
    def name(self) -> str:
        return "average"
    
    @property
    def description(self) -> str:
        return "计算数值列表的算术平均数：返回所有数值的平均值"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return AverageInput
    
    def validate_input(self, input_data: AverageInput) -> bool:
        """验证输入数据"""
        if not input_data.values:
            return False
        
        # 验证所有数值都是有限数
        return all(validate_finite_number(value) for value in input_data.values)
    
    async def execute(self, input_data: AverageInput) -> OperationResult:
        """执行平均数运算"""
        if not input_data.values:
            return OperationResult(
                success=False,
                error_message="错误：数值列表不能为空",
                operation_name=self.name
            )
        
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                error_message="输入包含无效数值（无穷大或NaN）",
                operation_name=self.name
            )
        
        try:
            # 计算平均数
            total = sum(input_data.values)
            count = len(input_data.values)
            average = total / count
            
            formatted_result = format_result(average)
            
            return OperationResult(
                success=True,
                result=formatted_result,
                operation_name=self.name
            )
        except ZeroDivisionError:
            # 理论上不应该发生，因为已经检查了列表非空
            return OperationResult(
                success=False,
                error_message="错误：数值列表为空",
                operation_name=self.name
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error_message=f"平均数运算失败: {str(e)}",
                operation_name=self.name
            )