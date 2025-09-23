"""
最大公约数运算操作测试
"""
import pytest
from calculator_mcp.operations.gcd import GCDOperation, GCDInput


class TestGCDOperation:
    """最大公约数运算操作测试类"""
    
    def setup_method(self):
        self.operation = GCDOperation()
    
    def test_operation_properties(self):
        """测试操作属性"""
        assert self.operation.name == "gcd"
        assert "最大公约数" in self.operation.description or "GCD" in self.operation.description
        assert self.operation.input_model == GCDInput
    
    @pytest.mark.asyncio
    async def test_basic_gcd_two_numbers(self):
        """测试两个数的最大公约数"""
        input_data = GCDInput(numbers=[12, 18])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 6
        assert result.metadata["gcd_notation"] == "GCD(12, 18)"
    
    @pytest.mark.asyncio
    async def test_coprime_numbers(self):
        """测试互质数"""
        input_data = GCDInput(numbers=[7, 13])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1
        assert result.metadata["is_coprime"] is True
    
    @pytest.mark.asyncio
    async def test_multiple_numbers(self):
        """测试多个数的最大公约数"""
        input_data = GCDInput(numbers=[12, 18, 24, 30])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 6
        assert result.metadata["count"] == 4
    
    @pytest.mark.asyncio
    async def test_one_is_multiple_of_other(self):
        """测试一个数是另一个数的倍数"""
        input_data = GCDInput(numbers=[15, 45])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 15
    
    @pytest.mark.asyncio
    async def test_negative_numbers(self):
        """测试负数"""
        input_data = GCDInput(numbers=[-12, 18])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 6  # GCD取绝对值
        assert result.metadata["absolute_numbers"] == [12, 18]
    
    @pytest.mark.asyncio
    async def test_both_negative(self):
        """测试两个负数"""
        input_data = GCDInput(numbers=[-12, -18])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 6
    
    @pytest.mark.asyncio
    async def test_with_zero(self):
        """测试包含0的情况"""
        input_data = GCDInput(numbers=[0, 12])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 12  # GCD(0, n) = n
    
    @pytest.mark.asyncio
    async def test_large_numbers(self):
        """测试大数"""
        input_data = GCDInput(numbers=[1000000, 500000])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 500000
    
    @pytest.mark.asyncio
    async def test_prime_numbers(self):
        """测试质数"""
        input_data = GCDInput(numbers=[17, 19, 23])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1
        assert result.metadata["is_coprime"] is True
    
    @pytest.mark.asyncio
    async def test_reduced_numbers(self):
        """测试化简后的数"""
        input_data = GCDInput(numbers=[12, 18, 24])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 6
        assert result.metadata["reduced_numbers"] == [2, 3, 4]
    
    @pytest.mark.asyncio
    async def test_identical_numbers(self):
        """测试相同的数"""
        input_data = GCDInput(numbers=[15, 15, 15])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 15
    
    @pytest.mark.asyncio
    async def test_single_number_error(self):
        """测试单个数字错误"""
        with pytest.raises(ValueError):
            GCDInput(numbers=[10])
    
    @pytest.mark.asyncio
    async def test_all_zeros_error(self):
        """测试全为0的错误"""
        with pytest.raises(ValueError):
            GCDInput(numbers=[0, 0, 0])
    
    @pytest.mark.asyncio
    async def test_empty_list_error(self):
        """测试空列表错误"""
        with pytest.raises(ValueError):
            GCDInput(numbers=[])
    
    def test_validate_input_valid(self):
        """测试输入验证：有效输入"""
        input_data = GCDInput(numbers=[12, 18])
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_insufficient(self):
        """测试输入验证：数字不足"""
        input_data = GCDInput.__new__(GCDInput)
        input_data.numbers = [10]
        assert self.operation.validate_input(input_data) is False
    
    def test_validate_input_all_zeros(self):
        """测试输入验证：全为0"""
        input_data = GCDInput.__new__(GCDInput)
        input_data.numbers = [0, 0]
        assert self.operation.validate_input(input_data) is False