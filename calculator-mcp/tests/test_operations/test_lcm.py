"""
最小公倍数运算操作测试
"""
import pytest
from calculator_mcp.operations.lcm import LCMOperation, LCMInput


class TestLCMOperation:
    """最小公倍数运算操作测试类"""
    
    def setup_method(self):
        self.operation = LCMOperation()
    
    def test_operation_properties(self):
        """测试操作属性"""
        assert self.operation.name == "lcm"
        assert "最小公倍数" in self.operation.description or "LCM" in self.operation.description
        assert self.operation.input_model == LCMInput
    
    @pytest.mark.asyncio
    async def test_basic_lcm_two_numbers(self):
        """测试两个数的最小公倍数"""
        input_data = LCMInput(numbers=[12, 18])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 36
        assert result.metadata["lcm_notation"] == "LCM(12, 18)"
    
    @pytest.mark.asyncio
    async def test_coprime_numbers(self):
        """测试互质数"""
        input_data = LCMInput(numbers=[7, 13])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 91  # 7 * 13
        assert result.metadata["gcd"] == 1
    
    @pytest.mark.asyncio
    async def test_multiple_numbers(self):
        """测试多个数的最小公倍数"""
        input_data = LCMInput(numbers=[4, 6, 8])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 24
        assert result.metadata["count"] == 3
    
    @pytest.mark.asyncio
    async def test_one_is_multiple_of_other(self):
        """测试一个数是另一个数的倍数"""
        input_data = LCMInput(numbers=[15, 45])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 45
    
    @pytest.mark.asyncio
    async def test_negative_numbers(self):
        """测试负数"""
        input_data = LCMInput(numbers=[-12, 18])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 36  # LCM取绝对值
        assert result.metadata["absolute_numbers"] == [12, 18]
    
    @pytest.mark.asyncio
    async def test_both_negative(self):
        """测试两个负数"""
        input_data = LCMInput(numbers=[-12, -18])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 36
    
    @pytest.mark.asyncio
    async def test_identical_numbers(self):
        """测试相同的数"""
        input_data = LCMInput(numbers=[15, 15])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 15
    
    @pytest.mark.asyncio
    async def test_powers_of_two(self):
        """测试2的幂"""
        input_data = LCMInput(numbers=[4, 8, 16])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 16
    
    @pytest.mark.asyncio
    async def test_prime_numbers(self):
        """测试质数"""
        input_data = LCMInput(numbers=[2, 3, 5])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 30  # 2 * 3 * 5
    
    @pytest.mark.asyncio
    async def test_large_numbers(self):
        """测试大数"""
        input_data = LCMInput(numbers=[100, 150])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 300
    
    @pytest.mark.asyncio
    async def test_relationship_with_gcd(self):
        """测试LCM和GCD的关系"""
        input_data = LCMInput(numbers=[12, 18])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 对于两个数：a * b = GCD(a,b) * LCM(a,b)
        # 12 * 18 = 6 * 36 = 216
        assert 12 * 18 == result.metadata["gcd"] * result.result
    
    @pytest.mark.asyncio
    async def test_consecutive_numbers(self):
        """测试连续数字"""
        input_data = LCMInput(numbers=[5, 6, 7])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 210  # 5 * 6 * 7
        assert result.metadata["gcd"] == 1
    
    @pytest.mark.asyncio
    async def test_with_zero_error(self):
        """测试包含0的错误"""
        with pytest.raises(ValueError):
            LCMInput(numbers=[0, 12])
    
    @pytest.mark.asyncio
    async def test_single_number_error(self):
        """测试单个数字错误"""
        with pytest.raises(ValueError):
            LCMInput(numbers=[10])
    
    @pytest.mark.asyncio
    async def test_empty_list_error(self):
        """测试空列表错误"""
        with pytest.raises(ValueError):
            LCMInput(numbers=[])
    
    def test_validate_input_valid(self):
        """测试输入验证：有效输入"""
        input_data = LCMInput(numbers=[12, 18])
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_with_zero(self):
        """测试输入验证：包含0"""
        input_data = LCMInput.__new__(LCMInput)
        input_data.numbers = [0, 12]
        assert self.operation.validate_input(input_data) is False
    
    def test_validate_input_insufficient(self):
        """测试输入验证：数字不足"""
        input_data = LCMInput.__new__(LCMInput)
        input_data.numbers = [10]
        assert self.operation.validate_input(input_data) is False