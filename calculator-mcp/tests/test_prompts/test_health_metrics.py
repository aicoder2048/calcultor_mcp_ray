"""
BMI与健康指标计算器Prompt测试
测试健康指标计算器的所有功能和边界情况
"""
import pytest
from calculator_mcp.prompts.health_metrics import (
    HealthMetricsPrompt,
    HealthMetricsArguments
)
from calculator_mcp.base.models import PromptResult


class TestHealthMetricsPrompt:
    """健康指标Prompt测试类"""
    
    @pytest.fixture
    def prompt(self):
        """创建Prompt实例"""
        return HealthMetricsPrompt()
    
    def test_prompt_properties(self, prompt):
        """测试Prompt基本属性"""
        assert prompt.name == "health_metrics"
        assert "BMI" in prompt.description
        assert prompt.arguments_schema == HealthMetricsArguments
    
    @pytest.mark.asyncio
    async def test_basic_bmi_calculation_metric(self, prompt):
        """测试基本BMI计算（公制）"""
        args = HealthMetricsArguments(
            height=170,  # 170厘米
            weight=70,   # 70公斤
            unit_system="metric",
            language="zh"
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert "BMI" in result.content
        assert "170" in result.content
        assert "70" in result.content
        assert "理想体重范围" in result.content
        assert result.metadata["height"] == 170
        assert result.metadata["weight"] == 70
    
    @pytest.mark.asyncio
    async def test_basic_bmi_calculation_imperial(self, prompt):
        """测试基本BMI计算（英制）"""
        args = HealthMetricsArguments(
            height=67,    # 67英寸 (约170厘米)
            weight=154,   # 154磅 (约70公斤)
            unit_system="imperial",
            language="en"
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert "BMI" in result.content
        assert "67" in result.content
        assert "154" in result.content
        assert "Ideal Weight Range" in result.content
        assert result.metadata["unit_system"] == "imperial"
    
    @pytest.mark.asyncio
    async def test_complete_health_metrics(self, prompt):
        """测试完整健康指标计算"""
        args = HealthMetricsArguments(
            height=175,
            weight=75,
            age=30,
            gender="male",
            activity_level="moderately_active",
            unit_system="metric",
            language="zh"
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert "BMI" in result.content
        assert "基础代谢率" in result.content
        assert "BMR" in result.content
        assert "每日热量需求" in result.content
        assert "TDEE" in result.content
        assert "中度活动" in result.content
        assert result.metadata["age"] == 30
        assert result.metadata["gender"] == "male"
        assert result.metadata["activity_level"] == "moderately_active"
    
    @pytest.mark.asyncio
    async def test_female_bmr_calculation(self, prompt):
        """测试女性BMR计算"""
        args = HealthMetricsArguments(
            height=165,
            weight=60,
            age=25,
            gender="female",
            activity_level="lightly_active",
            unit_system="metric",
            language="zh"
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert "BMR" in result.content
        assert "女性" in result.content or "female" in result.content.lower()
        assert "轻度活动" in result.content
    
    @pytest.mark.asyncio
    async def test_different_activity_levels(self, prompt):
        """测试不同活动水平"""
        activity_levels = [
            "sedentary",
            "lightly_active",
            "moderately_active",
            "very_active",
            "extra_active"
        ]
        
        for level in activity_levels:
            args = HealthMetricsArguments(
                height=180,
                weight=80,
                age=35,
                gender="male",
                activity_level=level,
                unit_system="metric",
                language="en"
            )
            
            result = await prompt.generate(args)
            
            assert result.success is True
            assert "TDEE" in result.content
            assert result.metadata["activity_level"] == level
    
    @pytest.mark.asyncio
    async def test_english_output(self, prompt):
        """测试英文输出"""
        args = HealthMetricsArguments(
            height=72,
            weight=180,
            age=40,
            gender="male",
            activity_level="very_active",
            unit_system="imperial",
            language="en"
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert "Health Metrics Analysis Report" in result.content
        assert "BMI Analysis" in result.content
        assert "Ideal Weight Range" in result.content
        assert "Basal Metabolic Rate" in result.content
        assert "Health Recommendations" in result.content
    
    @pytest.mark.asyncio
    async def test_chinese_output(self, prompt):
        """测试中文输出"""
        args = HealthMetricsArguments(
            height=168,
            weight=65,
            age=28,
            gender="female",
            activity_level="sedentary",
            unit_system="metric",
            language="zh"
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert "健康指标分析报告" in result.content
        assert "BMI分析" in result.content
        assert "理想体重范围" in result.content
        assert "基础代谢率" in result.content
        assert "健康建议" in result.content
    
    @pytest.mark.asyncio
    async def test_boundary_values_metric(self, prompt):
        """测试边界值（公制）"""
        # 最小值
        args_min = HealthMetricsArguments(
            height=30,
            weight=1,
            unit_system="metric"
        )
        result_min = await prompt.generate(args_min)
        assert result_min.success is True
        
        # 最大值
        args_max = HealthMetricsArguments(
            height=300,
            weight=1000,
            unit_system="metric"
        )
        result_max = await prompt.generate(args_max)
        assert result_max.success is True
    
    @pytest.mark.asyncio
    async def test_boundary_values_imperial(self, prompt):
        """测试边界值（英制）"""
        # 最小值
        args_min = HealthMetricsArguments(
            height=12,
            weight=2,
            unit_system="imperial"
        )
        result_min = await prompt.generate(args_min)
        assert result_min.success is True
        
        # 最大值
        args_max = HealthMetricsArguments(
            height=120,
            weight=2500,
            unit_system="imperial"
        )
        result_max = await prompt.generate(args_max)
        assert result_max.success is True
    
    @pytest.mark.asyncio
    async def test_invalid_parameters(self, prompt):
        """测试无效参数"""
        # 负数身高 - 应该在创建时就报错
        with pytest.raises(ValueError):
            HealthMetricsArguments(
                height=-170,
                weight=70
            )
        
        # 负数体重 - 应该在创建时就报错
        with pytest.raises(ValueError):
            HealthMetricsArguments(
                height=170,
                weight=-70
            )
        
        # 无效性别
        with pytest.raises(ValueError):
            HealthMetricsArguments(
                height=170,
                weight=70,
                gender="unknown"
            )
        
        # 无效活动水平
        with pytest.raises(ValueError):
            HealthMetricsArguments(
                height=170,
                weight=70,
                activity_level="super_active"
            )
        
        # 无效单位制
        with pytest.raises(ValueError):
            HealthMetricsArguments(
                height=170,
                weight=70,
                unit_system="unknown"
            )
        
        # 无效语言
        with pytest.raises(ValueError):
            HealthMetricsArguments(
                height=170,
                weight=70,
                language="fr"
            )
    
    @pytest.mark.asyncio
    async def test_age_boundaries(self, prompt):
        """测试年龄边界值"""
        # 最小年龄
        args_min_age = HealthMetricsArguments(
            height=170,
            weight=70,
            age=1,
            gender="male"
        )
        result_min = await prompt.generate(args_min_age)
        assert result_min.success is True
        
        # 最大年龄
        args_max_age = HealthMetricsArguments(
            height=170,
            weight=70,
            age=120,
            gender="female"
        )
        result_max = await prompt.generate(args_max_age)
        assert result_max.success is True
        
        # 无效年龄
        with pytest.raises(ValueError):
            HealthMetricsArguments(
                height=170,
                weight=70,
                age=0
            )
        
        with pytest.raises(ValueError):
            HealthMetricsArguments(
                height=170,
                weight=70,
                age=121
            )
    
    @pytest.mark.asyncio
    async def test_without_optional_parameters(self, prompt):
        """测试不包含可选参数的情况"""
        args = HealthMetricsArguments(
            height=170,
            weight=70
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert "BMI" in result.content
        assert "理想体重" in result.content
        # 不应包含BMR和TDEE（因为没有年龄和性别）
        assert "BMR" not in result.content or "基础代谢率" not in result.content
        assert "age" not in result.metadata
        assert "gender" not in result.metadata
    
    @pytest.mark.asyncio
    async def test_metadata_completeness(self, prompt):
        """测试元数据完整性"""
        args = HealthMetricsArguments(
            height=175,
            weight=75,
            age=30,
            gender="male",
            activity_level="moderately_active",
            unit_system="metric",
            language="zh"
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert result.metadata["height"] == 175
        assert result.metadata["weight"] == 75
        assert result.metadata["age"] == 30
        assert result.metadata["gender"] == "male"
        assert result.metadata["activity_level"] == "moderately_active"
        assert result.metadata["unit_system"] == "metric"
        assert result.metadata["language"] == "zh"
    
    def test_activity_multipliers(self, prompt):
        """测试活动水平系数"""
        assert prompt._get_activity_multiplier("sedentary") == 1.2
        assert prompt._get_activity_multiplier("lightly_active") == 1.375
        assert prompt._get_activity_multiplier("moderately_active") == 1.55
        assert prompt._get_activity_multiplier("very_active") == 1.725
        assert prompt._get_activity_multiplier("extra_active") == 1.9
        assert prompt._get_activity_multiplier("unknown") == 1.2  # 默认值
    
    def test_activity_descriptions(self, prompt):
        """测试活动水平描述"""
        # 中文描述
        assert "久坐" in prompt._get_activity_description_zh("sedentary")
        assert "轻度活动" in prompt._get_activity_description_zh("lightly_active")
        assert "中度活动" in prompt._get_activity_description_zh("moderately_active")
        assert "高度活动" in prompt._get_activity_description_zh("very_active")
        assert "极高活动" in prompt._get_activity_description_zh("extra_active")
        
        # 英文描述
        assert "Sedentary" in prompt._get_activity_description_en("sedentary")
        assert "Lightly active" in prompt._get_activity_description_en("lightly_active")
        assert "Moderately active" in prompt._get_activity_description_en("moderately_active")
        assert "Very active" in prompt._get_activity_description_en("very_active")
        assert "Extra active" in prompt._get_activity_description_en("extra_active")