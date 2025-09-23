"""
中位数运算操作测试
"""
import pytest
from calculator_mcp.operations.median import MedianOperation, MedianInput


class TestMedianOperation:
    """中位数运算操作测试类"""
    
    def setup_method(self):
        self.operation = MedianOperation()
    
    def test_operation_properties(self):
        """测试操作属性"""
        assert self.operation.name == "median"
        assert "中位数" in self.operation.description or "median" in self.operation.description.lower()
        assert self.operation.input_model == MedianInput
    
    @pytest.mark.asyncio
    async def test_odd_number_of_elements(self):
        """测试奇数个元素的中位数"""
        input_data = MedianInput(numbers=[1, 3, 5, 7, 9])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 5
        assert result.metadata["count"] == 5
        assert result.metadata["calculation_method"] == "奇数个元素，取中间值"
    
    @pytest.mark.asyncio
    async def test_even_number_of_elements(self):
        """测试偶数个元素的中位数"""
        input_data = MedianInput(numbers=[1, 2, 3, 4])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 2.5
        assert result.metadata["count"] == 4
        assert result.metadata["calculation_method"] == "偶数个元素，取中间两个数的平均值"
    
    @pytest.mark.asyncio
    async def test_single_element(self):
        """测试单个元素的中位数"""
        input_data = MedianInput(numbers=[42])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 42
        assert result.metadata["count"] == 1
    
    @pytest.mark.asyncio
    async def test_two_elements(self):
        """测试两个元素的中位数"""
        input_data = MedianInput(numbers=[10, 20])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 15
        assert result.metadata["count"] == 2
    
    @pytest.mark.asyncio
    async def test_unsorted_numbers(self):
        """测试未排序数列的中位数"""
        input_data = MedianInput(numbers=[5, 1, 9, 3, 7])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 5
        assert result.metadata["sorted_numbers"] == [1, 3, 5, 7, 9]
    
    @pytest.mark.asyncio
    async def test_negative_numbers(self):
        """测试包含负数的中位数"""
        input_data = MedianInput(numbers=[-5, -2, 0, 3, 7])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 0
    
    @pytest.mark.asyncio
    async def test_decimal_numbers(self):
        """测试小数的中位数"""
        input_data = MedianInput(numbers=[1.5, 2.3, 3.7, 4.1, 5.9])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 3.7
    
    @pytest.mark.asyncio
    async def test_duplicate_values(self):
        """测试重复值的中位数"""
        input_data = MedianInput(numbers=[1, 2, 2, 3, 3, 3, 4])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 3
    
    @pytest.mark.asyncio
    async def test_large_dataset(self):
        """测试大数据集的中位数"""
        numbers = list(range(1, 101))  # 1到100的数字
        input_data = MedianInput(numbers=numbers)
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.result == 50.5  # (50 + 51) / 2
    
    @pytest.mark.asyncio
    async def test_metadata_values(self):
        """测试元数据值"""
        input_data = MedianInput(numbers=[1, 2, 3, 4, 5])
        result = await self.operation.execute(input_data)
        
        assert result.success is True
        assert result.metadata["min"] == 1
        assert result.metadata["max"] == 5
        assert result.metadata["q1_approx"] == 2
        assert result.metadata["q3_approx"] == 4
    
    @pytest.mark.asyncio
    async def test_empty_list(self):
        """测试空列表"""
        with pytest.raises(ValueError):
            MedianInput(numbers=[])
    
    def test_validate_input_valid(self):
        """测试输入验证：有效输入"""
        input_data = MedianInput(numbers=[1, 2, 3])
        assert self.operation.validate_input(input_data) is True
    
    def test_validate_input_empty(self):
        """测试输入验证：空列表"""
        # 绕过 Pydantic 验证来测试
        input_data = MedianInput.__new__(MedianInput)
        input_data.numbers = []
        assert self.operation.validate_input(input_data) is False