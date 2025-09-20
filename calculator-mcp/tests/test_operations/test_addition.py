"""
加法运算单元测试
"""
import pytest
from calculator_mcp.operations.addition import AdditionOperation
from calculator_mcp.base.models import BinaryOperationInput


class TestAdditionOperation:
    def setup_method(self):
        self.operation = AdditionOperation()
    
    def test_properties(self):
        """测试运算属性"""
        assert self.operation.name == "add"
        assert "加法运算" in self.operation.description
        assert self.operation.input_model == BinaryOperationInput
    
    @pytest.mark.asyncio
    async def test_simple_addition(self):
        """测试简单加法"""
        input_data = BinaryOperationInput(a=5, b=3)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == 8.0
        assert result.operation_name == "add"
    
    @pytest.mark.asyncio
    async def test_negative_numbers(self):
        """测试负数加法"""
        input_data = BinaryOperationInput(a=-5, b=3)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == -2.0
    
    @pytest.mark.asyncio
    async def test_decimal_numbers(self):
        """测试小数加法"""
        input_data = BinaryOperationInput(a=2.5, b=1.5)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == 4.0
    
    @pytest.mark.asyncio
    async def test_zero_addition(self):
        """测试零加法"""
        input_data = BinaryOperationInput(a=0, b=5)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == 5.0
    
    def test_input_validation(self):
        """测试输入验证"""
        valid_input = BinaryOperationInput(a=5, b=3)
        assert self.operation.validate_input(valid_input) is True