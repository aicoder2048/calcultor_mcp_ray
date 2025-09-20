"""
平均数运算测试
"""
import pytest
import math
from calculator_mcp.operations.average import AverageOperation
from calculator_mcp.base.models import AverageInput, OperationResult


class TestAverageOperation:
    """平均数运算测试类"""
    
    def setup_method(self):
        """测试前置设置"""
        self.operation = AverageOperation()
    
    def test_operation_properties(self):
        """测试运算属性"""
        assert self.operation.name == "average"
        assert "平均数" in self.operation.description
        assert self.operation.input_model == AverageInput
    
    @pytest.mark.asyncio
    async def test_simple_average(self):
        """测试简单平均数计算"""
        input_data = AverageInput(values=[1.0, 2.0, 3.0, 4.0, 5.0])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 3.0
        assert result.operation_name == "average"
        assert result.error_message is None
    
    @pytest.mark.asyncio
    async def test_single_value(self):
        """测试单个值的平均数"""
        input_data = AverageInput(values=[42.0])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 42.0
        assert result.operation_name == "average"
    
    @pytest.mark.asyncio
    async def test_negative_numbers(self):
        """测试包含负数的平均数"""
        input_data = AverageInput(values=[-2.0, -1.0, 0.0, 1.0, 2.0])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0.0
        assert result.operation_name == "average"
    
    @pytest.mark.asyncio
    async def test_decimal_numbers(self):
        """测试小数的平均数"""
        input_data = AverageInput(values=[1.5, 2.5, 3.5])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 2.5
        assert result.operation_name == "average"
    
    @pytest.mark.asyncio
    async def test_large_numbers(self):
        """测试大数的平均数"""
        input_data = AverageInput(values=[1000000.0, 2000000.0, 3000000.0])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 2000000.0
        assert result.operation_name == "average"
    
    @pytest.mark.asyncio
    async def test_precision_handling(self):
        """测试精度处理"""
        input_data = AverageInput(values=[1.0, 2.0, 3.0])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 1+2+3 = 6, 6/3 = 2.0
        assert abs(result.result - 2.0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_empty_list(self):
        """测试空列表"""
        # 注意：Pydantic的min_length=1会阻止创建空列表的输入
        # 但我们可以测试运行时的空列表检查
        operation = AverageOperation()
        # 手动创建一个绕过验证的输入
        class MockInput:
            values = []
        
        mock_input = MockInput()
        result = await operation.execute(mock_input)
        
        assert result.success is False
        assert "不能为空" in result.error_message
        assert result.operation_name == "average"
    
    @pytest.mark.asyncio
    async def test_infinity_input(self):
        """测试无穷大输入"""
        input_data = AverageInput(values=[1.0, float('inf'), 3.0])
        result = await self.operation.execute(input_data)
        
        assert result.success is False
        assert "无效数值" in result.error_message
        assert result.operation_name == "average"
    
    @pytest.mark.asyncio
    async def test_nan_input(self):
        """测试NaN输入"""
        input_data = AverageInput(values=[1.0, float('nan'), 3.0])
        result = await self.operation.execute(input_data)
        
        assert result.success is False
        assert "无效数值" in result.error_message
        assert result.operation_name == "average"
    
    def test_validate_input_valid(self):
        """测试有效输入验证"""
        input_data = AverageInput(values=[1.0, 2.0, 3.0])
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_empty(self):
        """测试空输入验证"""
        class MockInput:
            values = []
        
        mock_input = MockInput()
        assert self.operation.validate_input(mock_input) is False
    
    def test_validate_input_infinity(self):
        """测试无穷大输入验证"""
        input_data = AverageInput(values=[1.0, float('inf')])
        assert self.operation.validate_input(input_data) is False
    
    def test_validate_input_nan(self):
        """测试NaN输入验证"""
        input_data = AverageInput(values=[1.0, float('nan')])
        assert self.operation.validate_input(input_data) is False
    
    @pytest.mark.asyncio
    async def test_zero_values(self):
        """测试全零值"""
        input_data = AverageInput(values=[0.0, 0.0, 0.0, 0.0])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0.0
        assert result.operation_name == "average"
    
    @pytest.mark.asyncio
    async def test_mixed_positive_negative(self):
        """测试正负数混合"""
        input_data = AverageInput(values=[-10.0, 5.0, 15.0, -5.0])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # (-10 + 5 + 15 - 5) / 4 = 5 / 4 = 1.25
        assert result.result == 1.25
        assert result.operation_name == "average"
    
    @pytest.mark.asyncio
    async def test_very_small_numbers(self):
        """测试非常小的数"""
        input_data = AverageInput(values=[1e-10, 2e-10, 3e-10])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 2e-10) < 1e-20
        assert result.operation_name == "average"