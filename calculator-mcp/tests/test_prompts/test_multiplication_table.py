"""
乘法口诀表Prompt测试
"""
import pytest
from pydantic import ValidationError
from calculator_mcp.prompts.multiplication_table import MultiplicationTablePrompt, MultiplicationTableArguments
from calculator_mcp.base.models import PromptResult


class TestMultiplicationTablePrompt:
    """乘法口诀表Prompt测试类"""
    
    def setup_method(self):
        """测试前置设置"""
        self.prompt = MultiplicationTablePrompt()
    
    def test_prompt_properties(self):
        """测试Prompt属性"""
        assert self.prompt.name == "multiplication_table"
        assert "乘法口诀表" in self.prompt.description
        assert self.prompt.arguments_schema == MultiplicationTableArguments
    
    @pytest.mark.asyncio
    async def test_basic_chinese_table_format(self):
        """测试基本中文表格格式"""
        args = MultiplicationTableArguments(
            size=3,
            start_number=1,
            language="zh",
            format="table"
        )
        result = await self.prompt.generate(args)
        
        assert result.success is True
        assert "乘法口诀表" in result.content
        assert "3x3" in result.content
        assert "起始数字: 1" in result.content
        assert "表格格式" in result.content
        assert "multiplication工具" in result.content
        assert result.prompt_name == "multiplication_table"
        assert result.metadata["size"] == 3
        assert result.metadata["start_number"] == 1
        assert result.metadata["language"] == "zh"
        assert result.metadata["format"] == "table"
    
    @pytest.mark.asyncio
    async def test_basic_english_list_format(self):
        """测试基本英文列表格式"""
        args = MultiplicationTableArguments(
            size=2,
            start_number=5,
            language="en",
            format="list"
        )
        result = await self.prompt.generate(args)
        
        assert result.success is True
        assert "Multiplication Table" in result.content
        assert "2x2" in result.content
        assert "Starting from: 5" in result.content
        assert "list format" in result.content
        assert "multiplication tool" in result.content
        assert result.prompt_name == "multiplication_table"
        assert result.metadata["size"] == 2
        assert result.metadata["start_number"] == 5
        assert result.metadata["language"] == "en"
        assert result.metadata["format"] == "list"
    
    @pytest.mark.asyncio
    async def test_negative_start_number(self):
        """测试负数起始值"""
        args = MultiplicationTableArguments(
            size=2,
            start_number=-3,
            language="zh",
            format="table"
        )
        result = await self.prompt.generate(args)
        
        assert result.success is True
        assert "起始数字: -3" in result.content
        assert "-3×-3" in result.content
        assert "-2×-2" in result.content
    
    @pytest.mark.asyncio
    async def test_maximum_size(self):
        """测试最大尺寸"""
        args = MultiplicationTableArguments(
            size=20,
            start_number=1,
            language="en",
            format="list"
        )
        result = await self.prompt.generate(args)
        
        assert result.success is True
        assert "20x20" in result.content
        assert "400 multiplication operations" in result.content
    
    @pytest.mark.asyncio
    async def test_minimum_size(self):
        """测试最小尺寸"""
        args = MultiplicationTableArguments(
            size=1,
            start_number=10,
            language="zh",
            format="table"
        )
        result = await self.prompt.generate(args)
        
        assert result.success is True
        assert "1x1" in result.content
        assert "1个乘法运算" in result.content
        assert "10×10" in result.content
    
    @pytest.mark.asyncio
    async def test_zero_start_number(self):
        """测试零起始值"""
        args = MultiplicationTableArguments(
            size=3,
            start_number=0,
            language="en",
            format="list"
        )
        result = await self.prompt.generate(args)
        
        assert result.success is True
        assert "Starting from: 0" in result.content
        assert "0×0" in result.content
        assert "2×2" in result.content
    
    def test_validate_arguments_valid(self):
        """测试有效参数验证"""
        args = MultiplicationTableArguments(
            size=5,
            start_number=1,
            language="zh",
            format="table"
        )
        assert self.prompt.validate_arguments(args) is True
    
    def test_validate_arguments_size_too_large(self):
        """测试尺寸过大验证"""
        with pytest.raises(ValidationError, match="Input should be less than or equal to 20"):
            MultiplicationTableArguments(
                size=25,  # 超过20的限制
                start_number=1,
                language="zh",
                format="table"
            )
    
    def test_validate_arguments_size_too_small(self):
        """测试尺寸过小验证"""
        with pytest.raises(ValidationError, match="Input should be greater than or equal to 1"):
            MultiplicationTableArguments(
                size=0,  # 小于1的限制
                start_number=1,
                language="zh",
                format="table"
            )
    
    def test_validate_arguments_start_number_too_large(self):
        """测试起始数字过大验证"""
        with pytest.raises(ValidationError, match="Input should be less than or equal to 100"):
            MultiplicationTableArguments(
                size=5,
                start_number=150,  # 超过100的限制
                language="zh",
                format="table"
            )
    
    def test_validate_arguments_start_number_too_small(self):
        """测试起始数字过小验证"""
        with pytest.raises(ValidationError, match="Input should be greater than or equal to -100"):
            MultiplicationTableArguments(
                size=5,
                start_number=-150,  # 小于-100的限制
                language="zh",
                format="table"
            )
    
    def test_validate_arguments_overflow_protection(self):
        """测试溢出保护验证"""
        args = MultiplicationTableArguments(
            size=20,
            start_number=100,  # 最大值组合，可能导致计算溢出
            language="zh",
            format="table"
        )
        # 100 + 20 - 1 = 119, 119^2 = 14161，应该通过
        assert self.prompt.validate_arguments(args) is True
        
        # 但是如果我们有更极端的情况...
        # 由于验证函数检查 abs(max_result) > 1e15
        # 我们需要构造一个会导致这种情况的参数组合
        
    @pytest.mark.asyncio 
    async def test_invalid_arguments_error(self):
        """测试无效参数错误处理"""
        # 使用直接构造绕过Pydantic验证
        class MockArgs:
            size = 25  # 超过限制
            start_number = 1
            language = "zh"
            format = "table"
        
        mock_args = MockArgs()
        result = await self.prompt.generate(mock_args)
        
        assert result.success is False
        assert "参数验证失败" in result.error_message
        assert result.prompt_name == "multiplication_table"
        assert result.content == ""
    
    def test_arguments_language_validation(self):
        """测试语言参数验证"""
        # 测试有效语言
        args_zh = MultiplicationTableArguments(size=3, language="zh")
        args_en = MultiplicationTableArguments(size=3, language="en")
        
        # 测试无效语言 - 这会被Pydantic验证器捕获
        with pytest.raises(ValueError, match="语言必须是"):
            MultiplicationTableArguments(size=3, language="fr")
    
    def test_arguments_format_validation(self):
        """测试格式参数验证"""
        # 测试有效格式
        args_table = MultiplicationTableArguments(size=3, format="table")
        args_list = MultiplicationTableArguments(size=3, format="list")
        
        # 测试无效格式 - 这会被Pydantic验证器捕获
        with pytest.raises(ValueError, match="格式必须是"):
            MultiplicationTableArguments(size=3, format="grid")
    
    @pytest.mark.asyncio
    async def test_large_calculation_count(self):
        """测试大计算量提示"""
        args = MultiplicationTableArguments(
            size=10,
            start_number=1,
            language="zh",
            format="table"
        )
        result = await self.prompt.generate(args)
        
        assert result.success is True
        assert "100个乘法运算" in result.content  # 10*10=100
    
    @pytest.mark.asyncio
    async def test_prompt_content_structure_chinese(self):
        """测试中文Prompt内容结构"""
        args = MultiplicationTableArguments(
            size=3,
            start_number=2,
            language="zh",
            format="table"
        )
        result = await self.prompt.generate(args)
        
        content = result.content
        assert "具体要求：" in content
        assert "multiplication工具计算" in content
        assert "从2开始，到4结束" in content
        assert "输出格式要求：" in content
        assert "使用表格格式展示" in content
        assert "9个乘法运算" in content
    
    @pytest.mark.asyncio
    async def test_prompt_content_structure_english(self):
        """测试英文Prompt内容结构"""
        args = MultiplicationTableArguments(
            size=4,
            start_number=0,
            language="en",
            format="list"
        )
        result = await self.prompt.generate(args)
        
        content = result.content
        assert "Requirements:" in content
        assert "multiplication tool" in content
        assert "Start from 0 and end at 3" in content
        assert "Output format requirements:" in content
        assert "Display in list format" in content
        assert "16 multiplication operations" in content
    
    @pytest.mark.asyncio
    async def test_boundary_calculations(self):
        """测试边界值计算"""
        # 测试包含计算范围的边界情况
        args = MultiplicationTableArguments(
            size=3,
            start_number=-1,
            language="zh",
            format="table"
        )
        result = await self.prompt.generate(args)
        
        assert result.success is True
        assert "-1×-1" in result.content
        assert "1×1" in result.content  # -1 + 3 - 1 = 1
        
    @pytest.mark.asyncio
    async def test_exception_handling(self):
        """测试异常处理"""
        # 创建一个会导致异常的Mock prompt
        class FailingPrompt(MultiplicationTablePrompt):
            def _generate_chinese_prompt(self, args):
                raise ValueError("测试异常")
        
        failing_prompt = FailingPrompt()
        args = MultiplicationTableArguments(
            size=3,
            start_number=1,
            language="zh",
            format="table"
        )
        
        result = await failing_prompt.generate(args)
        
        assert result.success is False
        assert "生成乘法口诀表Prompt失败" in result.error_message
        assert "测试异常" in result.error_message
        assert result.prompt_name == "multiplication_table"