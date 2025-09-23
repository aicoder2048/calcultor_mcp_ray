"""
单利计算操作测试
"""
import pytest
from calculator_mcp.operations.simple_interest import SimpleInterestOperation, SimpleInterestInput


class TestSimpleInterestOperation:
    
    def setup_method(self):
        self.operation = SimpleInterestOperation()
    
    def test_operation_properties(self):
        assert self.operation.name == "simple_interest"
        assert "单利" in self.operation.description
        assert self.operation.input_model == SimpleInterestInput
    
    @pytest.mark.asyncio
    async def test_basic_interest_calculation(self):
        input_data = SimpleInterestInput(principal=1000, rate=5, time=1)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 50
        assert result.metadata["total_amount"] == 1050
    
    @pytest.mark.asyncio
    async def test_multi_year_interest(self):
        input_data = SimpleInterestInput(principal=1000, rate=5, time=3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 150
        assert result.metadata["total_amount"] == 1150
    
    @pytest.mark.asyncio
    async def test_decimal_rate(self):
        input_data = SimpleInterestInput(principal=1000, rate=4.5, time=2)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 90
    
    @pytest.mark.asyncio
    async def test_decimal_time(self):
        input_data = SimpleInterestInput(principal=1000, rate=6, time=0.5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 30
    
    @pytest.mark.asyncio
    async def test_large_principal(self):
        input_data = SimpleInterestInput(principal=100000, rate=3, time=5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 15000
    
    @pytest.mark.asyncio
    async def test_high_interest_rate(self):
        input_data = SimpleInterestInput(principal=5000, rate=12, time=2)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1200
    
    @pytest.mark.asyncio
    async def test_zero_principal_error(self):
        with pytest.raises(ValueError):
            SimpleInterestInput(principal=0, rate=5, time=1)
    
    @pytest.mark.asyncio
    async def test_negative_principal_error(self):
        with pytest.raises(ValueError):
            SimpleInterestInput(principal=-1000, rate=5, time=1)
    
    @pytest.mark.asyncio
    async def test_zero_rate_error(self):
        with pytest.raises(ValueError):
            SimpleInterestInput(principal=1000, rate=0, time=1)
    
    @pytest.mark.asyncio
    async def test_zero_time_error(self):
        with pytest.raises(ValueError):
            SimpleInterestInput(principal=1000, rate=5, time=0)
    
    @pytest.mark.asyncio
    async def test_metadata_values(self):
        input_data = SimpleInterestInput(principal=2000, rate=4, time=3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["principal"] == 2000
        assert result.metadata["rate_percent"] == 4
        assert result.metadata["rate_decimal"] == 0.04
        assert result.metadata["time_years"] == 3
        assert result.metadata["interest"] == 240
    
    def test_validate_input_valid(self):
        input_data = SimpleInterestInput(principal=1000, rate=5, time=1)
        assert self.operation.validate_input(input_data) is True