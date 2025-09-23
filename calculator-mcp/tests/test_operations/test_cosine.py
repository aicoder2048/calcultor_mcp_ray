"""
余弦函数运算操作测试
"""
import pytest
import math
from calculator_mcp.operations.cosine import CosineOperation, CosineInput


class TestCosineOperation:
    
    def setup_method(self):
        self.operation = CosineOperation()
    
    def test_operation_properties(self):
        assert self.operation.name == "cosine"
        assert "余弦" in self.operation.description
        assert self.operation.input_model == CosineInput
    
    @pytest.mark.asyncio
    async def test_cosine_0_degrees(self):
        input_data = CosineInput(angle=0, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 1.0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_cosine_60_degrees(self):
        input_data = CosineInput(angle=60, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0.5) < 1e-10
    
    @pytest.mark.asyncio
    async def test_cosine_90_degrees(self):
        input_data = CosineInput(angle=90, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_cosine_180_degrees(self):
        input_data = CosineInput(angle=180, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - (-1.0)) < 1e-10
    
    @pytest.mark.asyncio
    async def test_cosine_270_degrees(self):
        input_data = CosineInput(angle=270, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_cosine_360_degrees(self):
        input_data = CosineInput(angle=360, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 1.0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_cosine_radian_mode(self):
        input_data = CosineInput(angle=0, unit="radian")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 1.0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_cosine_radian_pi(self):
        input_data = CosineInput(angle=math.pi, unit="radian")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - (-1.0)) < 1e-10
    
    @pytest.mark.asyncio
    async def test_cosine_negative_angle(self):
        input_data = CosineInput(angle=-60, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0.5) < 1e-10
    
    @pytest.mark.asyncio
    async def test_cosine_infinity_error(self):
        input_data = CosineInput(angle=float('inf'), unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is False
    
    def test_validate_input_valid(self):
        input_data = CosineInput(angle=45, unit="degree")
        assert self.operation.validate_input(input_data) is True