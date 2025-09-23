"""
方差运算操作测试
"""
import pytest
import math
from calculator_mcp.operations.variance import VarianceOperation, VarianceInput


class TestVarianceOperation:
    """方差运算操作测试类"""
    
    def setup_method(self):
        self.operation = VarianceOperation()
    
    def test_operation_properties(self):
        """测试操作属性"""
        assert self.operation.name == "variance"
        assert "方差" in self.operation.description
        assert self.operation.input_model == VarianceInput
    
    @pytest.mark.asyncio
    async def test_sample_variance(self):
        """测试样本方差"""
        input_data = VarianceInput(
            numbers=[2, 4, 4, 4, 5, 5, 7, 9],
            is_sample=True
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 样本方差应该是 4.0（标准差2.0的平方）
        assert abs(result.result - 4.0) < 1e-10
        assert result.metadata["variance_type"] == "样本方差"
        assert result.metadata["divisor"] == 7
        assert abs(result.metadata["standard_deviation"] - 2.0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_population_variance(self):
        """测试总体方差"""
        input_data = VarianceInput(
            numbers=[2, 4, 4, 4, 5, 5, 7, 9],
            is_sample=False
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 总体方差应该是 3.5
        assert abs(result.result - 3.5) < 1e-10
        assert result.metadata["variance_type"] == "总体方差"
        assert result.metadata["divisor"] == 8
    
    @pytest.mark.asyncio
    async def test_two_numbers(self):
        """测试两个数字的方差"""
        input_data = VarianceInput(
            numbers=[1, 5],
            is_sample=True
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 两个数的样本方差 = (4^2)/1 = 16/1 = 8
        assert abs(result.result - 8.0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_identical_values(self):
        """测试相同值的方差"""
        input_data = VarianceInput(
            numbers=[5, 5, 5, 5, 5],
            is_sample=True
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0  # 所有值相同，方差为0
        assert result.metadata["standard_deviation"] == 0
    
    @pytest.mark.asyncio
    async def test_negative_numbers(self):
        """测试负数的方差"""
        input_data = VarianceInput(
            numbers=[-2, -1, 0, 1, 2],
            is_sample=False
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 总体方差 = 2
        assert abs(result.result - 2.0) < 1e-10
    
    @pytest.mark.asyncio
    async def test_decimal_numbers(self):
        """测试小数的方差"""
        input_data = VarianceInput(
            numbers=[1.5, 2.5, 3.5, 4.5],
            is_sample=True
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 等差数列的方差
        expected = 5/3  # 约1.667
        assert abs(result.result - expected) < 1e-10
    
    @pytest.mark.asyncio
    async def test_relationship_with_std(self):
        """测试方差与标准差的关系"""
        input_data = VarianceInput(
            numbers=[1, 2, 3, 4, 5],
            is_sample=True
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 验证：标准差 = sqrt(方差)
        std = result.metadata["standard_deviation"]
        assert abs(std ** 2 - result.result) < 1e-10
    
    @pytest.mark.asyncio
    async def test_metadata_values(self):
        """测试元数据值"""
        input_data = VarianceInput(
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
        assert result.metadata["sum_squared_differences"] > 0
    
    @pytest.mark.asyncio
    async def test_large_variance(self):
        """测试大方差"""
        input_data = VarianceInput(
            numbers=[1, 1000],
            is_sample=True
        )
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        # 方差 = (999^2)/1
        expected = 998001
        assert abs(result.result - expected) < 1e-6
    
    @pytest.mark.asyncio
    async def test_single_number_error(self):
        """测试单个数字错误"""
        with pytest.raises(ValueError):
            VarianceInput(numbers=[5])
    
    @pytest.mark.asyncio
    async def test_empty_list_error(self):
        """测试空列表错误"""
        with pytest.raises(ValueError):
            VarianceInput(numbers=[])
    
    def test_validate_input_valid(self):
        """测试输入验证：有效输入"""
        input_data = VarianceInput(numbers=[1, 2, 3])
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_insufficient(self):
        """测试输入验证：数字不足"""
        input_data = VarianceInput.__new__(VarianceInput)
        input_data.numbers = [5]
        assert self.operation.validate_input(input_data) is False