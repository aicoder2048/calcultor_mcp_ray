"""
对数运算操作测试
"""
import pytest
import math
from calculator_mcp.operations.logarithm import LogarithmOperation, LogarithmInput


class TestLogarithmOperation:
    """对数运算操作测试类"""
    
    def setup_method(self):
        self.operation = LogarithmOperation()
    
    def test_operation_properties(self):
        """测试操作属性"""
        assert self.operation.name == "logarithm"
        assert "对数" in self.operation.description
        assert self.operation.input_model == LogarithmInput
    
    @pytest.mark.asyncio
    async def test_natural_logarithm(self):
        """测试自然对数"""
        input_data = LogarithmInput(number=math.e)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 1.0) < 1e-10
        assert result.metadata["log_type"] == "natural"
        assert "ln" in result.metadata["notation"]
    
    @pytest.mark.asyncio
    async def test_common_logarithm(self):
        """测试常用对数"""
        input_data = LogarithmInput(number=100, base=10)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 2.0) < 1e-10
        assert result.metadata["log_type"] == "common"
        assert "log₁₀" in result.metadata["notation"]
    
    @pytest.mark.asyncio
    async def test_custom_base_logarithm(self):
        """测试自定义底数对数"""
        input_data = LogarithmInput(number=8, base=2)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 3.0) < 1e-10
        assert result.metadata["log_type"] == "custom"
        assert "log_2" in result.metadata["notation"]
    
    @pytest.mark.asyncio
    async def test_logarithm_of_one(self):
        """测试1的对数（任何底数都为0）"""
        input_data = LogarithmInput(number=1, base=10)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0
    
    @pytest.mark.asyncio
    async def test_logarithm_base_equals_number(self):
        """测试底数等于数字（结果为1）"""
        input_data = LogarithmInput(number=5, base=5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 1.0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_fractional_logarithm(self):
        """测试分数的对数"""
        input_data = LogarithmInput(number=0.5, base=2)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - (-1.0)) < 1e-10
    
    @pytest.mark.asyncio
    async def test_invalid_input_negative_number(self):
        """测试无效输入：负数"""
        with pytest.raises(ValueError):
            LogarithmInput(number=-1)
    
    @pytest.mark.asyncio
    async def test_invalid_input_zero(self):
        """测试无效输入：零"""
        with pytest.raises(ValueError):
            LogarithmInput(number=0)
    
    @pytest.mark.asyncio
    async def test_invalid_input_base_one(self):
        """测试无效输入：底数为1"""
        with pytest.raises(ValueError):
            LogarithmInput(number=10, base=1)
    
    @pytest.mark.asyncio
    async def test_invalid_input_negative_base(self):
        """测试无效输入：负底数"""
        with pytest.raises(ValueError):
            LogarithmInput(number=10, base=-2)
    
    @pytest.mark.asyncio
    async def test_large_numbers(self):
        """测试大数值"""
        input_data = LogarithmInput(number=1000000, base=10)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 6.0) < 1e-10
    
    def test_validate_input_valid(self):
        """测试输入验证：有效输入"""
        input_data = LogarithmInput(number=10, base=2)
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_invalid(self):
        """测试输入验证：无效输入"""
        # 这里需要绕过 Pydantic 验证来测试 validate_input 方法
        input_data = LogarithmInput.__new__(LogarithmInput)
        input_data.number = -1
        input_data.base = 2
        assert self.operation.validate_input(input_data) is False