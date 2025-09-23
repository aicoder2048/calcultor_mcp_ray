"""
正弦函数运算操作测试
"""
import pytest
import math
from calculator_mcp.operations.sine import SineOperation, SineInput


class TestSineOperation:
    
    def setup_method(self):
        self.operation = SineOperation()
    
    def test_operation_properties(self):
        assert self.operation.name == "sine"
        assert "正弦" in self.operation.description
        assert self.operation.input_model == SineInput
    
    @pytest.mark.asyncio
    async def test_sine_0_degrees(self):
        input_data = SineInput(angle=0, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_sine_30_degrees(self):
        input_data = SineInput(angle=30, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0.5) < 1e-10
    
    @pytest.mark.asyncio
    async def test_sine_45_degrees(self):
        input_data = SineInput(angle=45, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - math.sqrt(2)/2) < 1e-10
    
    @pytest.mark.asyncio
    async def test_sine_60_degrees(self):
        input_data = SineInput(angle=60, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - math.sqrt(3)/2) < 1e-10
    
    @pytest.mark.asyncio
    async def test_sine_90_degrees(self):
        input_data = SineInput(angle=90, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 1.0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_sine_180_degrees(self):
        input_data = SineInput(angle=180, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_sine_270_degrees(self):
        input_data = SineInput(angle=270, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - (-1.0)) < 1e-10
    
    @pytest.mark.asyncio
    async def test_sine_360_degrees(self):
        input_data = SineInput(angle=360, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_sine_negative_angle(self):
        input_data = SineInput(angle=-30, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - (-0.5)) < 1e-10
    
    @pytest.mark.asyncio
    async def test_sine_radian_mode(self):
        input_data = SineInput(angle=math.pi/2, unit="radian")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 1.0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_sine_radian_pi(self):
        input_data = SineInput(angle=math.pi, unit="radian")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_sine_large_angle(self):
        input_data = SineInput(angle=390, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0.5) < 1e-10
    
    @pytest.mark.asyncio
    async def test_sine_infinity_error(self):
        input_data = SineInput(angle=float('inf'), unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is False
        assert "有限数值" in result.error_message
    
    @pytest.mark.asyncio
    async def test_sine_metadata(self):
        input_data = SineInput(angle=30, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["angle"] == 30
        assert result.metadata["unit"] == "degree"
        assert "angle_radians" in result.metadata
    
    def test_validate_input_valid(self):
        input_data = SineInput(angle=45, unit="degree")
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_invalid_unit(self):
        with pytest.raises(ValueError):
            SineInput(angle=45, unit="invalid")