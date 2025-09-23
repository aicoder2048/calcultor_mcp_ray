"""
幂运算操作测试
"""
import pytest
from calculator_mcp.operations.power import PowerOperation, PowerInput


class TestPowerOperation:
    """幂运算操作测试类"""
    
    def setup_method(self):
        self.operation = PowerOperation()
    
    def test_operation_properties(self):
        """测试操作属性"""
        assert self.operation.name == "power"
        assert "幂" in self.operation.description or "power" in self.operation.description.lower()
        assert self.operation.input_model == PowerInput
    
    @pytest.mark.asyncio
    async def test_positive_integer_power(self):
        """测试正整数幂"""
        input_data = PowerInput(base=2, exponent=3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 8
        assert result.metadata["calculation"] == "2^3"
    
    @pytest.mark.asyncio
    async def test_negative_exponent(self):
        """测试负指数"""
        input_data = PowerInput(base=2, exponent=-3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0.125) < 1e-10
    
    @pytest.mark.asyncio
    async def test_fractional_exponent(self):
        """测试分数指数"""
        input_data = PowerInput(base=4, exponent=0.5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 2
    
    @pytest.mark.asyncio
    async def test_zero_exponent(self):
        """测试零指数"""
        input_data = PowerInput(base=5, exponent=0)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1
    
    @pytest.mark.asyncio
    async def test_one_as_base(self):
        """测试底数为1"""
        input_data = PowerInput(base=1, exponent=100)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1
    
    @pytest.mark.asyncio
    async def test_zero_base_positive_exponent(self):
        """测试底数为0，正指数"""
        input_data = PowerInput(base=0, exponent=5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0
    
    @pytest.mark.asyncio
    async def test_zero_base_negative_exponent(self):
        """测试底数为0，负指数（应该失败）"""
        input_data = PowerInput(base=0, exponent=-2)
        result = await self.operation.execute(input_data)
        
        assert result.success is False
        assert "0的负数次方无定义" in result.error_message
    
    @pytest.mark.asyncio
    async def test_negative_base_integer_exponent(self):
        """测试负底数，整数指数"""
        input_data = PowerInput(base=-2, exponent=3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == -8
    
    @pytest.mark.asyncio
    async def test_negative_base_fractional_exponent(self):
        """测试负底数，分数指数（应该失败）"""
        input_data = PowerInput(base=-2, exponent=0.5)
        result = await self.operation.execute(input_data)
        
        assert result.success is False
        assert "复数" in result.error_message
    
    @pytest.mark.asyncio
    async def test_large_numbers(self):
        """测试大数值"""
        input_data = PowerInput(base=10, exponent=10)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 10000000000
    
    def test_validate_input_valid(self):
        """测试输入验证：有效输入"""
        input_data = PowerInput(base=2, exponent=3)
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_zero_negative_power(self):
        """测试输入验证：0的负次方"""
        input_data = PowerInput(base=0, exponent=-1)
        assert self.operation.validate_input(input_data) is False
    
    def test_validate_input_negative_fractional_power(self):
        """测试输入验证：负数的分数次方"""
        input_data = PowerInput(base=-2, exponent=1.5)
        assert self.operation.validate_input(input_data) is False