"""
绝对值运算操作测试
"""
import pytest
from calculator_mcp.operations.absolute import AbsoluteOperation, AbsoluteInput


class TestAbsoluteOperation:
    """绝对值运算操作测试类"""
    
    def setup_method(self):
        self.operation = AbsoluteOperation()
    
    def test_operation_properties(self):
        """测试操作属性"""
        assert self.operation.name == "absolute"
        assert "绝对值" in self.operation.description or "|x|" in self.operation.description
        assert self.operation.input_model == AbsoluteInput
    
    @pytest.mark.asyncio
    async def test_positive_number(self):
        """测试正数的绝对值"""
        input_data = AbsoluteInput(number=5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 5
        assert result.metadata["is_changed"] is False
        assert result.metadata["notation"] == "|5|"
    
    @pytest.mark.asyncio
    async def test_negative_number(self):
        """测试负数的绝对值"""
        input_data = AbsoluteInput(number=-5)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 5
        assert result.metadata["is_changed"] is True
        assert result.metadata["notation"] == "|-5|"
    
    @pytest.mark.asyncio
    async def test_zero(self):
        """测试零的绝对值"""
        input_data = AbsoluteInput(number=0)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0
        assert result.metadata["is_changed"] is False
    
    @pytest.mark.asyncio
    async def test_decimal_positive(self):
        """测试正小数的绝对值"""
        input_data = AbsoluteInput(number=3.14)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 3.14
        assert result.metadata["is_changed"] is False
    
    @pytest.mark.asyncio
    async def test_decimal_negative(self):
        """测试负小数的绝对值"""
        input_data = AbsoluteInput(number=-3.14)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 3.14
        assert result.metadata["is_changed"] is True
    
    @pytest.mark.asyncio
    async def test_large_positive_number(self):
        """测试大正数的绝对值"""
        input_data = AbsoluteInput(number=1e10)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1e10
        assert result.metadata["is_changed"] is False
    
    @pytest.mark.asyncio
    async def test_large_negative_number(self):
        """测试大负数的绝对值"""
        input_data = AbsoluteInput(number=-1e10)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 1e10
        assert result.metadata["is_changed"] is True
    
    @pytest.mark.asyncio
    async def test_very_small_negative_number(self):
        """测试很小的负数"""
        input_data = AbsoluteInput(number=-0.00001)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0.00001
        assert result.metadata["is_changed"] is True
    
    def test_validate_input_always_valid(self):
        """测试输入验证：绝对值对所有实数都有效"""
        test_cases = [
            AbsoluteInput(number=0),
            AbsoluteInput(number=5),
            AbsoluteInput(number=-5),
            AbsoluteInput(number=3.14),
            AbsoluteInput(number=-3.14),
            AbsoluteInput(number=1e100),
            AbsoluteInput(number=-1e100)
        ]
        
        for input_data in test_cases:
            assert self.operation.validate_input(input_data) is True