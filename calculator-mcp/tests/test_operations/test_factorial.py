"""
阶乘运算操作测试
"""
import pytest
import math
from calculator_mcp.operations.factorial import FactorialOperation, FactorialInput


class TestFactorialOperation:
    
    def setup_method(self):
        self.operation = FactorialOperation()
    
    def test_operation_properties(self):
        assert self.operation.name == "factorial"
        assert "阶乘" in self.operation.description
        assert self.operation.input_model == FactorialInput
    
    @pytest.mark.asyncio
    async def test_factorial_0(self):
        input_data = FactorialInput(n=0)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1
    
    @pytest.mark.asyncio
    async def test_factorial_1(self):
        input_data = FactorialInput(n=1)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1
    
    @pytest.mark.asyncio
    async def test_factorial_5(self):
        input_data = FactorialInput(n=5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 120
    
    @pytest.mark.asyncio
    async def test_factorial_10(self):
        input_data = FactorialInput(n=10)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 3628800
    
    @pytest.mark.asyncio
    async def test_factorial_20(self):
        input_data = FactorialInput(n=20)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        expected = math.factorial(20)
        assert result.result == expected
    
    @pytest.mark.asyncio
    async def test_factorial_metadata(self):
        input_data = FactorialInput(n=5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["n"] == 5
        assert result.metadata["digit_count"] == 3
        assert "calculation" in result.metadata
    
    @pytest.mark.asyncio
    async def test_factorial_large_number(self):
        input_data = FactorialInput(n=100)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        expected = math.factorial(100)
        assert result.result == float(expected)
    
    @pytest.mark.asyncio
    async def test_negative_number_error(self):
        with pytest.raises(ValueError):
            FactorialInput(n=-1)
    
    @pytest.mark.asyncio
    async def test_too_large_number_error(self):
        input_data = FactorialInput(n=200)
        result = await self.operation.execute(input_data)
        
        assert result.success is False
        assert "过大" in result.error_message
    
    def test_validate_input_valid(self):
        input_data = FactorialInput(n=10)
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_too_large(self):
        input_data = FactorialInput(n=171)
        assert self.operation.validate_input(input_data) is False