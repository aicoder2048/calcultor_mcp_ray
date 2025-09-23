"""
排列运算操作测试
"""
import pytest
import math
from calculator_mcp.operations.permutation import PermutationOperation, PermutationInput


class TestPermutationOperation:
    
    def setup_method(self):
        self.operation = PermutationOperation()
    
    def test_operation_properties(self):
        assert self.operation.name == "permutation"
        assert "排列" in self.operation.description
        assert self.operation.input_model == PermutationInput
    
    @pytest.mark.asyncio
    async def test_permutation_p_5_2(self):
        input_data = PermutationInput(n=5, r=2)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 20
    
    @pytest.mark.asyncio
    async def test_permutation_p_5_5(self):
        input_data = PermutationInput(n=5, r=5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 120
    
    @pytest.mark.asyncio
    async def test_permutation_p_10_3(self):
        input_data = PermutationInput(n=10, r=3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 720
    
    @pytest.mark.asyncio
    async def test_permutation_p_n_0(self):
        input_data = PermutationInput(n=5, r=0)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1
    
    @pytest.mark.asyncio
    async def test_permutation_p_0_0(self):
        input_data = PermutationInput(n=0, r=0)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1
    
    @pytest.mark.asyncio
    async def test_permutation_metadata(self):
        input_data = PermutationInput(n=6, r=3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["n"] == 6
        assert result.metadata["r"] == 3
        assert "formula" in result.metadata
        assert "meaning" in result.metadata
    
    @pytest.mark.asyncio
    async def test_r_greater_than_n_error(self):
        input_data = PermutationInput(n=5, r=5)
        input_data_invalid = PermutationInput.__new__(PermutationInput)
        object.__setattr__(input_data_invalid, 'n', 5)
        object.__setattr__(input_data_invalid, 'r', 10)
        
        result = await self.operation.execute(input_data_invalid)
        assert result.success is False
    
    @pytest.mark.asyncio
    async def test_negative_n_error(self):
        with pytest.raises(ValueError):
            PermutationInput(n=-5, r=2)
    
    @pytest.mark.asyncio
    async def test_negative_r_error(self):
        with pytest.raises(ValueError):
            PermutationInput(n=5, r=-2)
    
    def test_validate_input_valid(self):
        input_data = PermutationInput(n=10, r=5)
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_r_greater_than_n(self):
        input_data = PermutationInput.__new__(PermutationInput)
        object.__setattr__(input_data, 'n', 3)
        object.__setattr__(input_data, 'r', 5)
        assert self.operation.validate_input(input_data) is False