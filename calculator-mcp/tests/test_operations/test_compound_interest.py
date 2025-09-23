"""
复利计算操作测试
"""
import pytest
from calculator_mcp.operations.compound_interest import CompoundInterestOperation, CompoundInterestInput


class TestCompoundInterestOperation:
    
    def setup_method(self):
        self.operation = CompoundInterestOperation()
    
    def test_operation_properties(self):
        assert self.operation.name == "compound_interest"
        assert "复利" in self.operation.description
        assert self.operation.input_model == CompoundInterestInput
    
    @pytest.mark.asyncio
    async def test_annual_compounding(self):
        input_data = CompoundInterestInput(principal=1000, rate=5, time=1, frequency=1)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 1050) < 0.01
    
    @pytest.mark.asyncio
    async def test_quarterly_compounding(self):
        input_data = CompoundInterestInput(principal=1000, rate=8, time=2, frequency=4)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        expected = 1000 * (1 + 0.08/4) ** (4*2)
        assert abs(result.result - expected) < 0.01
    
    @pytest.mark.asyncio
    async def test_monthly_compounding(self):
        input_data = CompoundInterestInput(principal=5000, rate=6, time=1, frequency=12)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        expected = 5000 * (1 + 0.06/12) ** 12
        assert abs(result.result - expected) < 0.01
    
    @pytest.mark.asyncio
    async def test_daily_compounding(self):
        input_data = CompoundInterestInput(principal=1000, rate=5, time=1, frequency=365)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        expected = 1000 * (1 + 0.05/365) ** 365
        assert abs(result.result - expected) < 0.01
    
    @pytest.mark.asyncio
    async def test_multi_year_compounding(self):
        input_data = CompoundInterestInput(principal=10000, rate=7, time=5, frequency=1)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        expected = 10000 * (1.07 ** 5)
        assert abs(result.result - expected) < 0.01
    
    @pytest.mark.asyncio
    async def test_interest_amount_calculation(self):
        input_data = CompoundInterestInput(principal=2000, rate=5, time=3, frequency=1)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        interest = result.metadata["interest"]
        assert abs(interest - (result.result - 2000)) < 0.01
    
    @pytest.mark.asyncio
    async def test_frequency_description(self):
        input_data = CompoundInterestInput(principal=1000, rate=5, time=1, frequency=12)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["frequency_description"] == "月"
    
    @pytest.mark.asyncio
    async def test_total_periods(self):
        input_data = CompoundInterestInput(principal=1000, rate=5, time=2, frequency=4)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["total_periods"] == 8
    
    @pytest.mark.asyncio
    async def test_zero_principal_error(self):
        with pytest.raises(ValueError):
            CompoundInterestInput(principal=0, rate=5, time=1, frequency=1)
    
    @pytest.mark.asyncio
    async def test_zero_frequency_error(self):
        with pytest.raises(ValueError):
            CompoundInterestInput(principal=1000, rate=5, time=1, frequency=0)
    
    def test_validate_input_valid(self):
        input_data = CompoundInterestInput(principal=1000, rate=5, time=1, frequency=12)
        assert self.operation.validate_input(input_data) is True