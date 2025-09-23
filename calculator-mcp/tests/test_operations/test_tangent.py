"""
正切函数运算操作测试
"""
import pytest
import math
from calculator_mcp.operations.tangent import TangentOperation, TangentInput


class TestTangentOperation:
    
    def setup_method(self):
        self.operation = TangentOperation()
    
    def test_operation_properties(self):
        assert self.operation.name == "tangent"
        assert "正切" in self.operation.description
        assert self.operation.input_model == TangentInput
    
    @pytest.mark.asyncio
    async def test_tangent_0_degrees(self):
        input_data = TangentInput(angle=0, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_tangent_45_degrees(self):
        input_data = TangentInput(angle=45, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 1.0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_tangent_60_degrees(self):
        input_data = TangentInput(angle=60, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - math.sqrt(3)) < 1e-10
    
    @pytest.mark.asyncio
    async def test_tangent_90_degrees_undefined(self):
        input_data = TangentInput(angle=90, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is False
        assert "无定义" in result.error_message
    
    @pytest.mark.asyncio
    async def test_tangent_180_degrees(self):
        input_data = TangentInput(angle=180, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_tangent_270_degrees_undefined(self):
        input_data = TangentInput(angle=270, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is False
        assert "无定义" in result.error_message
    
    @pytest.mark.asyncio
    async def test_tangent_radian_mode(self):
        input_data = TangentInput(angle=math.pi/4, unit="radian")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 1.0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_tangent_negative_angle(self):
        input_data = TangentInput(angle=-45, unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - (-1.0)) < 1e-10
    
    @pytest.mark.asyncio
    async def test_tangent_infinity_error(self):
        input_data = TangentInput(angle=float('inf'), unit="degree")
        result = await self.operation.execute(input_data)
        
        assert result.success is False
    
    def test_validate_input_valid(self):
        input_data = TangentInput(angle=45, unit="degree")
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_90_degrees(self):
        input_data = TangentInput(angle=90, unit="degree")
        assert self.operation.validate_input(input_data) is False