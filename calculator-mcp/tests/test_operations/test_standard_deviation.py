"""
标准差运算操作测试
"""
import pytest
import math
from calculator_mcp.operations.standard_deviation import StandardDeviationOperation, StandardDeviationInput


class TestStandardDeviationOperation:
    """标准差运算操作测试类"""
    
    def setup_method(self):
        self.operation = StandardDeviationOperation()
    
    def test_operation_properties(self):
        """测试操作属性"""
        assert self.operation.name == "standard_deviation"
        assert "标准差" in self.operation.description
        assert self.operation.input_model == StandardDeviationInput
    
    @pytest.mark.asyncio
    async def test_sample_standard_deviation(self):
        """测试样本标准差"""
        input_data = StandardDeviationInput(
            numbers=[2, 4, 4, 4, 5, 5, 7, 9],
            is_sample=True
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 样本标准差应该是 2.0
        assert abs(result.result - 2.0) < 1e-10
        assert result.metadata["std_type"] == "样本标准差"
        assert result.metadata["divisor"] == 7
    
    @pytest.mark.asyncio
    async def test_population_standard_deviation(self):
        """测试总体标准差"""
        input_data = StandardDeviationInput(
            numbers=[2, 4, 4, 4, 5, 5, 7, 9],
            is_sample=False
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 总体标准差应该约为 1.87
        assert abs(result.result - 1.8708286933869707) < 1e-10
        assert result.metadata["std_type"] == "总体标准差"
        assert result.metadata["divisor"] == 8
    
    @pytest.mark.asyncio
    async def test_two_numbers(self):
        """测试两个数字的标准差"""
        input_data = StandardDeviationInput(
            numbers=[1, 5],
            is_sample=True
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 两个数的样本标准差 = |5-1|/sqrt(2) * sqrt(2) = 4/sqrt(2) * sqrt(2) = 4 * sqrt(1/2) * sqrt(2) = 2.828...
        expected = math.sqrt(8)  # sqrt((4^2)/(2-1)) = sqrt(16/1) = sqrt(16) = 4... 实际是 sqrt(8)
        assert abs(result.result - expected) < 1e-10
    
    @pytest.mark.asyncio
    async def test_identical_values(self):
        """测试相同值的标准差"""
        input_data = StandardDeviationInput(
            numbers=[5, 5, 5, 5, 5],
            is_sample=True
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0  # 所有值相同，标准差为0
    
    @pytest.mark.asyncio
    async def test_negative_numbers(self):
        """测试负数的标准差"""
        input_data = StandardDeviationInput(
            numbers=[-2, -1, 0, 1, 2],
            is_sample=False
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 总体标准差 = sqrt(2)
        assert abs(result.result - math.sqrt(2)) < 1e-10
    
    @pytest.mark.asyncio
    async def test_decimal_numbers(self):
        """测试小数的标准差"""
        input_data = StandardDeviationInput(
            numbers=[1.5, 2.5, 3.5, 4.5],
            is_sample=True
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 等差数列的标准差
        expected = math.sqrt(5/3)  # 约1.29
        assert abs(result.result - expected) < 1e-10
    
    @pytest.mark.asyncio
    async def test_metadata_values(self):
        """测试元数据值"""
        input_data = StandardDeviationInput(
            numbers=[1, 2, 3, 4, 5],
            is_sample=True
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["count"] == 5
        assert result.metadata["mean"] == 3
        assert result.metadata["min"] == 1
        assert result.metadata["max"] == 5
        assert result.metadata["range"] == 4
        assert result.metadata["coefficient_of_variation"] is not None
    
    @pytest.mark.asyncio
    async def test_coefficient_of_variation(self):
        """测试变异系数"""
        input_data = StandardDeviationInput(
            numbers=[10, 20, 30],
            is_sample=True
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 变异系数 = (标准差 / 平均值) * 100
        cv = result.metadata["coefficient_of_variation"]
        assert cv is not None
        assert cv == (result.result / 20) * 100
    
    @pytest.mark.asyncio
    async def test_single_number_error(self):
        """测试单个数字错误"""
        with pytest.raises(ValueError):
            StandardDeviationInput(numbers=[5])
    
    @pytest.mark.asyncio
    async def test_empty_list_error(self):
        """测试空列表错误"""
        with pytest.raises(ValueError):
            StandardDeviationInput(numbers=[])
    
    def test_validate_input_valid(self):
        """测试输入验证：有效输入"""
        input_data = StandardDeviationInput(numbers=[1, 2, 3])
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_insufficient(self):
        """测试输入验证：数字不足"""
        input_data = StandardDeviationInput.__new__(StandardDeviationInput)
        input_data.numbers = [5]
        assert self.operation.validate_input(input_data) is False