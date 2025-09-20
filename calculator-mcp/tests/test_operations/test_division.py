"""
除法运算单元测试
"""
import pytest
from calculator_mcp.operations.division import DivisionOperation
from calculator_mcp.base.models import BinaryOperationInput


class TestDivisionOperation:
    def setup_method(self):
        self.operation = DivisionOperation()
    
    def test_properties(self):
        """测试运算属性"""
        assert self.operation.name == "divide"
        assert "除法运算" in self.operation.description
        assert self.operation.input_model == BinaryOperationInput
    
    @pytest.mark.asyncio
    async def test_simple_division(self):
        """测试简单除法"""
        input_data = BinaryOperationInput(a=10, b=2)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == 5.0
        assert result.operation_name == "divide"
    
    @pytest.mark.asyncio
    async def test_division_with_remainder(self):
        """测试有余数的除法"""
        input_data = BinaryOperationInput(a=10, b=3)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert abs(result.result - 3.3333333333) < 1e-9
    
    @pytest.mark.asyncio
    async def test_division_by_zero(self):
        """测试除零错误"""
        input_data = BinaryOperationInput(a=10, b=0)
        result = await self.operation.execute(input_data)
        assert result.success is False
        assert "除数不能为零" in result.error_message
        assert result.result is None
    
    @pytest.mark.asyncio
    async def test_negative_division(self):
        """测试负数除法"""
        input_data = BinaryOperationInput(a=-10, b=2)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == -5.0
    
    @pytest.mark.asyncio
    async def test_decimal_division(self):
        """测试小数除法"""
        input_data = BinaryOperationInput(a=7.5, b=2.5)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == 3.0
    
    def test_input_validation(self):
        """测试输入验证"""
        valid_input = BinaryOperationInput(a=10, b=2)
        assert self.operation.validate_input(valid_input) is True
        
        invalid_input = BinaryOperationInput(a=10, b=0)
        assert self.operation.validate_input(invalid_input) is False