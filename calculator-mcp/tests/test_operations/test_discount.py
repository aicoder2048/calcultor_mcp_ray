"""
折扣计算操作测试
"""
import pytest
from calculator_mcp.operations.discount import DiscountOperation, DiscountInput


class TestDiscountOperation:
    
    def setup_method(self):
        self.operation = DiscountOperation()
    
    def test_operation_properties(self):
        assert self.operation.name == "discount"
        assert "折扣" in self.operation.description
        assert self.operation.input_model == DiscountInput
    
    @pytest.mark.asyncio
    async def test_20_percent_discount(self):
        input_data = DiscountInput(original_price=100, discount_percent=20)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 80
        assert result.metadata["discount_amount"] == 20
    
    @pytest.mark.asyncio
    async def test_50_percent_discount(self):
        input_data = DiscountInput(original_price=200, discount_percent=50)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 100
        assert result.metadata["savings"] == 100
    
    @pytest.mark.asyncio
    async def test_10_percent_discount(self):
        input_data = DiscountInput(original_price=500, discount_percent=10)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 450
        assert result.metadata["discount_amount"] == 50
    
    @pytest.mark.asyncio
    async def test_no_discount(self):
        input_data = DiscountInput(original_price=100, discount_percent=0)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 100
        assert result.metadata["discount_amount"] == 0
    
    @pytest.mark.asyncio
    async def test_100_percent_discount(self):
        input_data = DiscountInput(original_price=150, discount_percent=100)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0
        assert result.metadata["discount_amount"] == 150
    
    @pytest.mark.asyncio
    async def test_decimal_discount(self):
        input_data = DiscountInput(original_price=100, discount_percent=15.5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 84.5
    
    @pytest.mark.asyncio
    async def test_actual_pay_percent(self):
        input_data = DiscountInput(original_price=100, discount_percent=25)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["actual_pay_percent"] == 75
    
    @pytest.mark.asyncio
    async def test_savings_calculation(self):
        input_data = DiscountInput(original_price=250, discount_percent=30)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["savings"] == 75
        assert result.metadata["savings_percent"] == 30
    
    @pytest.mark.asyncio
    async def test_zero_price_error(self):
        with pytest.raises(ValueError):
            DiscountInput(original_price=0, discount_percent=20)
    
    @pytest.mark.asyncio
    async def test_negative_price_error(self):
        with pytest.raises(ValueError):
            DiscountInput(original_price=-100, discount_percent=20)
    
    @pytest.mark.asyncio
    async def test_negative_discount_error(self):
        with pytest.raises(ValueError):
            DiscountInput(original_price=100, discount_percent=-10)
    
    @pytest.mark.asyncio
    async def test_over_100_discount_error(self):
        with pytest.raises(ValueError):
            DiscountInput(original_price=100, discount_percent=110)
    
    def test_validate_input_valid(self):
        input_data = DiscountInput(original_price=100, discount_percent=20)
        assert self.operation.validate_input(input_data) is True