"""
质数判断操作测试
"""
import pytest
from calculator_mcp.operations.prime_check import PrimeCheckOperation, PrimeCheckInput


class TestPrimeCheckOperation:
    
    def setup_method(self):
        self.operation = PrimeCheckOperation()
    
    def test_operation_properties(self):
        assert self.operation.name == "prime_check"
        assert "质数" in self.operation.description
        assert self.operation.input_model == PrimeCheckInput
    
    @pytest.mark.asyncio
    async def test_prime_2(self):
        input_data = PrimeCheckInput(number=2)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1.0
        assert result.metadata["is_prime"] is True
    
    @pytest.mark.asyncio
    async def test_prime_3(self):
        input_data = PrimeCheckInput(number=3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["is_prime"] is True
    
    @pytest.mark.asyncio
    async def test_prime_7(self):
        input_data = PrimeCheckInput(number=7)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["is_prime"] is True
    
    @pytest.mark.asyncio
    async def test_not_prime_4(self):
        input_data = PrimeCheckInput(number=4)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0.0
        assert result.metadata["is_prime"] is False
        assert 2 in result.metadata["factors"]
    
    @pytest.mark.asyncio
    async def test_not_prime_9(self):
        input_data = PrimeCheckInput(number=9)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["is_prime"] is False
        assert 3 in result.metadata["factors"]
    
    @pytest.mark.asyncio
    async def test_large_prime_97(self):
        input_data = PrimeCheckInput(number=97)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["is_prime"] is True
    
    @pytest.mark.asyncio
    async def test_not_prime_100(self):
        input_data = PrimeCheckInput(number=100)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["is_prime"] is False
        assert len(result.metadata["factors"]) > 0
    
    @pytest.mark.asyncio
    async def test_prime_101(self):
        input_data = PrimeCheckInput(number=101)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["is_prime"] is True
        assert result.metadata["factors"] == []
    
    @pytest.mark.asyncio
    async def test_large_composite(self):
        input_data = PrimeCheckInput(number=1000)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["is_prime"] is False
    
    @pytest.mark.asyncio
    async def test_number_1_error(self):
        with pytest.raises(ValueError):
            PrimeCheckInput(number=1)
    
    @pytest.mark.asyncio
    async def test_number_0_error(self):
        with pytest.raises(ValueError):
            PrimeCheckInput(number=0)
    
    @pytest.mark.asyncio
    async def test_result_text_metadata(self):
        input_data = PrimeCheckInput(number=13)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert "是质数" in result.metadata["result_text"]
    
    def test_validate_input_valid(self):
        input_data = PrimeCheckInput(number=17)
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_too_large(self):
        input_data = PrimeCheckInput.__new__(PrimeCheckInput)
        object.__setattr__(input_data, 'number', 10**16)
        assert self.operation.validate_input(input_data) is False