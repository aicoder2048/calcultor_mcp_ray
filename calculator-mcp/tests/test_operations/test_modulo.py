"""
取模运算操作测试
"""
import pytest
from calculator_mcp.operations.modulo import ModuloOperation, ModuloInput


class TestModuloOperation:
    """取模运算操作测试类"""
    
    def setup_method(self):
        self.operation = ModuloOperation()
    
    def test_operation_properties(self):
        """测试操作属性"""
        assert self.operation.name == "modulo"
        assert "取模" in self.operation.description or "mod" in self.operation.description
        assert self.operation.input_model == ModuloInput
    
    @pytest.mark.asyncio
    async def test_basic_modulo(self):
        """测试基础取模运算"""
        input_data = ModuloInput(dividend=10, divisor=3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1
        assert result.metadata["quotient"] == 3
        assert result.metadata["notation"] == "10 mod 3"
    
    @pytest.mark.asyncio
    async def test_exact_division(self):
        """测试整除情况"""
        input_data = ModuloInput(dividend=12, divisor=4)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0
        assert result.metadata["quotient"] == 3
    
    @pytest.mark.asyncio
    async def test_negative_dividend(self):
        """测试负被除数"""
        input_data = ModuloInput(dividend=-10, divisor=3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # Python的模运算：-10 mod 3 = 2
        assert result.result == 2
        assert result.metadata["quotient"] == -4
    
    @pytest.mark.asyncio
    async def test_negative_divisor(self):
        """测试负除数"""
        input_data = ModuloInput(dividend=10, divisor=-3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # Python的模运算：10 mod -3 = -2
        assert result.result == -2
        assert result.metadata["quotient"] == -4
    
    @pytest.mark.asyncio
    async def test_both_negative(self):
        """测试两个负数"""
        input_data = ModuloInput(dividend=-10, divisor=-3)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # Python的模运算：-10 mod -3 = -1
        assert result.result == -1
        assert result.metadata["quotient"] == 3
    
    @pytest.mark.asyncio
    async def test_decimal_numbers(self):
        """测试小数取模"""
        input_data = ModuloInput(dividend=10.5, divisor=3.2)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 10.5 mod 3.2 应该约为 0.9
        assert abs(result.result - 0.9) < 1e-10
    
    @pytest.mark.asyncio
    async def test_dividend_smaller_than_divisor(self):
        """测试被除数小于除数"""
        input_data = ModuloInput(dividend=3, divisor=10)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 3
        assert result.metadata["quotient"] == 0
    
    @pytest.mark.asyncio
    async def test_verification(self):
        """测试验证公式"""
        input_data = ModuloInput(dividend=17, divisor=5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 验证：dividend = quotient * divisor + remainder
        verification = result.metadata["quotient"] * input_data.divisor + result.result
        assert abs(verification - input_data.dividend) < 1e-10
        assert abs(result.metadata["verification"] - input_data.dividend) < 1e-10
    
    @pytest.mark.asyncio
    async def test_modulo_one(self):
        """测试模1运算"""
        input_data = ModuloInput(dividend=7.5, divisor=1)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0.5
    
    @pytest.mark.asyncio
    async def test_division_by_zero(self):
        """测试除以零错误"""
        with pytest.raises(ValueError):
            ModuloInput(dividend=10, divisor=0)
    
    @pytest.mark.asyncio
    async def test_large_numbers(self):
        """测试大数值"""
        input_data = ModuloInput(dividend=1000000, divisor=7)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 5
    
    def test_validate_input_valid(self):
        """测试输入验证：有效输入"""
        input_data = ModuloInput(dividend=10, divisor=3)
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_zero_divisor(self):
        """测试输入验证：除数为零"""
        input_data = ModuloInput.__new__(ModuloInput)
        input_data.dividend = 10
        input_data.divisor = 0
        assert self.operation.validate_input(input_data) is False