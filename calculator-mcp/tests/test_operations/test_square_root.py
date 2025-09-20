"""
平方根运算单元测试
"""
import pytest
from calculator_mcp.operations.square_root import SquareRootOperation
from calculator_mcp.base.models import UnaryOperationInput


class TestSquareRootOperation:
    def setup_method(self):
        self.operation = SquareRootOperation()
    
    def test_properties(self):
        """测试运算属性"""
        assert self.operation.name == "square_root"
        assert "平方根" in self.operation.description
        assert self.operation.input_model == UnaryOperationInput
    
    @pytest.mark.asyncio
    async def test_perfect_square(self):
        """测试完全平方数"""
        input_data = UnaryOperationInput(value=16)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == 4.0
        assert result.operation_name == "square_root"
    
    @pytest.mark.asyncio
    async def test_zero_square_root(self):
        """测试零的平方根"""
        input_data = UnaryOperationInput(value=0)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == 0.0
    
    @pytest.mark.asyncio
    async def test_decimal_square_root(self):
        """测试小数的平方根"""
        input_data = UnaryOperationInput(value=2.25)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == 1.5
    
    @pytest.mark.asyncio
    async def test_negative_square_root(self):
        """测试负数平方根错误"""
        input_data = UnaryOperationInput(value=-4)
        result = await self.operation.execute(input_data)
        assert result.success is False
        assert "负数的平方根" in result.error_message
        assert result.result is None
    
    @pytest.mark.asyncio
    async def test_large_number(self):
        """测试大数的平方根"""
        input_data = UnaryOperationInput(value=100)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == 10.0
    
    def test_input_validation(self):
        """测试输入验证"""
        valid_input = UnaryOperationInput(value=9)
        assert self.operation.validate_input(valid_input) is True
        
        invalid_input = UnaryOperationInput(value=-4)
        assert self.operation.validate_input(invalid_input) is False