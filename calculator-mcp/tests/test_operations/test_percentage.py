"""
百分比运算操作测试
"""
import pytest
from calculator_mcp.operations.percentage import PercentageOperation, PercentageInput


class TestPercentageOperation:
    """百分比运算操作测试类"""
    
    def setup_method(self):
        self.operation = PercentageOperation()
    
    def test_operation_properties(self):
        """测试操作属性"""
        assert self.operation.name == "percentage"
        assert "百分比" in self.operation.description or "percentage" in self.operation.description.lower()
        assert self.operation.input_model == PercentageInput
    
    @pytest.mark.asyncio
    async def test_basic_percentage(self):
        """测试基础百分比计算"""
        input_data = PercentageInput(
            calculation_type="percentage",
            value=25,
            reference=100
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 25.0
        assert result.metadata["unit"] == "%"
    
    @pytest.mark.asyncio
    async def test_change_rate_positive(self):
        """测试正变化率"""
        input_data = PercentageInput(
            calculation_type="change",
            value=150,
            reference=100
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 50.0  # 50% 增长
        assert result.metadata["unit"] == "%"
    
    @pytest.mark.asyncio
    async def test_change_rate_negative(self):
        """测试负变化率"""
        input_data = PercentageInput(
            calculation_type="change",
            value=75,
            reference=100
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == -25.0  # 25% 下降
        assert result.metadata["unit"] == "%"
    
    @pytest.mark.asyncio
    async def test_portion_calculation(self):
        """测试比例计算"""
        input_data = PercentageInput(
            calculation_type="portion",
            value=3,
            reference=4
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0.75
        assert result.metadata["unit"] == "ratio"
    
    @pytest.mark.asyncio
    async def test_increase_percentage(self):
        """测试百分比增加"""
        input_data = PercentageInput(
            calculation_type="increase",
            value=20,  # 增加20%
            reference=100
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 120.0
    
    @pytest.mark.asyncio
    async def test_decrease_percentage(self):
        """测试百分比减少"""
        input_data = PercentageInput(
            calculation_type="decrease",
            value=20,  # 减少20%
            reference=100
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 80.0
    
    @pytest.mark.asyncio
    async def test_decimal_percentage(self):
        """测试小数百分比"""
        input_data = PercentageInput(
            calculation_type="percentage",
            value=33.33,
            reference=100
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert abs(result.result - 33.33) < 1e-10
    
    @pytest.mark.asyncio
    async def test_over_100_percent(self):
        """测试超过100%的情况"""
        input_data = PercentageInput(
            calculation_type="percentage",
            value=150,
            reference=100
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 150.0
    
    @pytest.mark.asyncio
    async def test_invalid_reference_zero(self):
        """测试无效输入：参考值为0"""
        with pytest.raises(ValueError):
            PercentageInput(
                calculation_type="percentage",
                value=50,
                reference=0
            )
    
    @pytest.mark.asyncio
    async def test_invalid_calculation_type(self):
        """测试无效的计算类型"""
        with pytest.raises(ValueError):
            PercentageInput(
                calculation_type="invalid",
                value=50,
                reference=100
            )
    
    @pytest.mark.asyncio
    async def test_negative_reference_change(self):
        """测试负参考值的变化率"""
        input_data = PercentageInput(
            calculation_type="change",
            value=-50,
            reference=-100
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 50.0  # 从-100到-50是50%的增长
    
    def test_validate_input_valid(self):
        """测试输入验证：有效输入"""
        input_data = PercentageInput(
            calculation_type="percentage",
            value=50,
            reference=100
        )
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_zero_reference(self):
        """测试输入验证：参考值为0"""
        input_data = PercentageInput.__new__(PercentageInput)
        input_data.calculation_type = "percentage"
        input_data.value = 50
        input_data.reference = 0
        assert self.operation.validate_input(input_data) is False