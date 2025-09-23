"""
组合运算操作测试
"""
import pytest
import math
from calculator_mcp.operations.combination import CombinationOperation, CombinationInput


class TestCombinationOperation:
    
    def setup_method(self):
        self.operation = CombinationOperation()
    
    def test_operation_properties(self):
        assert self.operation.name == "combination"
        assert "组合" in self.operation.description
        assert self.operation.input_model == CombinationInput
    
    @pytest.mark.asyncio
    async def test_combination_c_5_2(self):
        input_data = CombinationInput(n=5, r=2)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 10
    
    @pytest.mark.asyncio
    async def test_combination_c_5_3(self):
        input_data = CombinationInput(n=5, r=3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 10
    
    @pytest.mark.asyncio
    async def test_combination_c_10_5(self):
        input_data = CombinationInput(n=10, r=5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 252
    
    @pytest.mark.asyncio
    async def test_combination_c_n_0(self):
        input_data = CombinationInput(n=7, r=0)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1
    
    @pytest.mark.asyncio
    async def test_combination_c_n_n(self):
        input_data = CombinationInput(n=5, r=5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1
    
    @pytest.mark.asyncio
    async def test_combination_symmetry(self):
        result1 = await self.operation.execute(CombinationInput(n=8, r=3))
        result2 = await self.operation.execute(CombinationInput(n=8, r=5))
        
        assert result1.success is True
        assert result2.success is True
        assert result1.result == result2.result
    
    @pytest.mark.asyncio
    async def test_combination_metadata(self):
        input_data = CombinationInput(n=6, r=2)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["n"] == 6
        assert result.metadata["r"] == 2
        assert "formula" in result.metadata
        assert "symmetry" in result.metadata
    
    @pytest.mark.asyncio
    async def test_r_greater_than_n_error(self):
        input_data_invalid = CombinationInput.__new__(CombinationInput)
        object.__setattr__(input_data_invalid, 'n', 5)
        object.__setattr__(input_data_invalid, 'r', 10)
        
        result = await self.operation.execute(input_data_invalid)
        assert result.success is False
    
    @pytest.mark.asyncio
    async def test_negative_values_error(self):
        with pytest.raises(ValueError):
            CombinationInput(n=-5, r=2)
    
    def test_validate_input_valid(self):
        input_data = CombinationInput(n=10, r=3)
        assert self.operation.validate_input(input_data) is True