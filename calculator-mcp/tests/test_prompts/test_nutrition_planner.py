"""
营养配餐计算器Prompt测试
测试营养配餐计算器的所有功能和边界情况
"""
import pytest
from calculator_mcp.prompts.nutrition_planner import (
    NutritionPlannerPrompt,
    NutritionPlannerArguments
)
from calculator_mcp.base.models import PromptResult


class TestNutritionPlannerPrompt:
    """营养配餐Prompt测试类"""
    
    @pytest.fixture
    def prompt(self):
        """创建Prompt实例"""
        return NutritionPlannerPrompt()
    
    def test_prompt_properties(self, prompt):
        """测试Prompt基本属性"""
        assert prompt.name == "nutrition_planner"
        assert "营养配餐" in prompt.description or "nutrition" in prompt.description.lower()
        assert prompt.arguments_schema == NutritionPlannerArguments
    
    @pytest.mark.asyncio
    async def test_basic_nutrition_planning(self, prompt):
        """测试基本营养配餐计算"""
        args = NutritionPlannerArguments(
            height=170,
            weight=70,
            age=30,
            gender="male",
            activity_level="moderately_active",
            goal="maintain"
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert "BMR" in result.content or "基础代谢率" in result.content
        assert "TDEE" in result.content or "总热量消耗" in result.content
        assert "蛋白质" in result.content or "protein" in result.content.lower()
        assert "碳水化合物" in result.content or "carbohydrate" in result.content.lower()
        assert "脂肪" in result.content or "fat" in result.content.lower()
        assert result.metadata["height"] == 170
        assert result.metadata["weight"] == 70
        assert result.metadata["goal"] == "maintain"
    
    @pytest.mark.asyncio
    async def test_weight_loss_goal(self, prompt):
        """测试减重目标"""
        args = NutritionPlannerArguments(
            height=165,
            weight=80,
            age=35,
            gender="female",
            activity_level="lightly_active",
            goal="lose_weight",
            target_weight=70,
            timeline_weeks=20
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert "减重" in result.content or "weight loss" in result.content.lower()
        assert "目标体重" in result.content or "target weight" in result.content.lower()
        assert "300" in result.content or "500" in result.content  # 热量赤字
        assert result.metadata["target_weight"] == 70
        assert result.metadata["timeline_weeks"] == 20
    
    @pytest.mark.asyncio
    async def test_muscle_building_goal(self, prompt):
        """测试增肌目标"""
        args = NutritionPlannerArguments(
            height=175,
            weight=75,
            age=25,
            gender="male",
            activity_level="very_active",
            goal="gain_muscle"
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert ("增肌" in result.content or "muscle" in result.content.lower() or 
                "gain_muscle" in result.content)
        assert "2.0" in result.content  # 高蛋白需求 2.0g/kg
        assert result.metadata["goal"] == "gain_muscle"
    
    @pytest.mark.asyncio
    async def test_dietary_restrictions(self, prompt):
        """测试饮食限制"""
        args = NutritionPlannerArguments(
            height=168,
            weight=65,
            age=28,
            gender="female",
            goal="maintain",
            dietary_restrictions=["vegetarian", "gluten_free"]
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert ("素食" in result.content or "vegetarian" in result.content.lower())
        assert ("无麸质" in result.content or "gluten" in result.content.lower())
        assert result.metadata["dietary_restrictions"] == ["vegetarian", "gluten_free"]
    
    @pytest.mark.asyncio
    async def test_multiple_meals_per_day(self, prompt):
        """测试不同餐次数量"""
        for meals in [3, 4, 5, 6]:
            args = NutritionPlannerArguments(
                height=170,
                weight=70,
                age=30,
                gender="male",
                meals_per_day=meals
            )
            
            result = await prompt.generate(args)
            
            assert result.success is True
            assert result.metadata["meals_per_day"] == meals
            # 检查是否包含餐次分配内容
            assert ("餐" in result.content or "meal" in result.content.lower())
    
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
            args = NutritionPlannerArguments(
                height=175,
                weight=75,
                age=30,
                gender="male",
                activity_level=level
            )
            
            result = await prompt.generate(args)
            
            assert result.success is True
            assert result.metadata["activity_level"] == level
    
    @pytest.mark.asyncio
    async def test_english_output(self, prompt):
        """测试英文输出"""
        args = NutritionPlannerArguments(
            height=180,
            weight=80,
            age=25,
            gender="male",
            goal="gain_weight",
            target_weight=85,
            language="en"
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert "Nutrition Requirements" in result.content or "nutrition" in result.content.lower()
        assert "BMR" in result.content
        assert "TDEE" in result.content
        assert "Protein" in result.content
        assert "Carbohydrates" in result.content
        assert "Fat" in result.content
        assert result.metadata["language"] == "en"
    
    @pytest.mark.asyncio
    async def test_chinese_output(self, prompt):
        """测试中文输出"""
        args = NutritionPlannerArguments(
            height=165,
            weight=60,
            age=22,
            gender="female",
            goal="gain_muscle",
            language="zh"
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        assert "营养需求" in result.content
        assert "基础代谢率" in result.content
        assert "蛋白质" in result.content
        assert "碳水化合物" in result.content
        assert "脂肪" in result.content
        assert result.metadata["language"] == "zh"
    
    @pytest.mark.asyncio
    async def test_all_dietary_goals(self, prompt):
        """测试所有饮食目标"""
        goals = ["maintain", "lose_weight", "gain_weight", "gain_muscle"]
        
        for goal in goals:
            args = NutritionPlannerArguments(
                height=170,
                weight=70,
                age=30,
                gender="male",
                goal=goal
            )
            
            result = await prompt.generate(args)
            
            assert result.success is True
            assert result.metadata["goal"] == goal
    
    @pytest.mark.asyncio
    async def test_boundary_values(self, prompt):
        """测试边界值"""
        # 最小值（稍高于边界）
        args_min = NutritionPlannerArguments(
            height=101,
            weight=31,
            age=1,
            gender="female",
            meals_per_day=3
        )
        result_min = await prompt.generate(args_min)
        assert result_min.success is True
        
        # 最大值
        args_max = NutritionPlannerArguments(
            height=250,
            weight=200,
            age=120,
            gender="male",
            meals_per_day=6,
            timeline_weeks=104
        )
        result_max = await prompt.generate(args_max)
        assert result_max.success is True
    
    @pytest.mark.asyncio
    async def test_invalid_parameters(self, prompt):
        """测试无效参数"""
        # 身高过小
        with pytest.raises(ValueError):
            NutritionPlannerArguments(
                height=50,
                weight=70,
                age=30,
                gender="male"
            )
        
        # 体重过大
        with pytest.raises(ValueError):
            NutritionPlannerArguments(
                height=170,
                weight=300,
                age=30,
                gender="male"
            )
        
        # 无效性别
        with pytest.raises(ValueError):
            NutritionPlannerArguments(
                height=170,
                weight=70,
                age=30,
                gender="unknown"
            )
        
        # 无效活动水平
        with pytest.raises(ValueError):
            NutritionPlannerArguments(
                height=170,
                weight=70,
                age=30,
                gender="male",
                activity_level="super_active"
            )
        
        # 无效饮食目标
        with pytest.raises(ValueError):
            NutritionPlannerArguments(
                height=170,
                weight=70,
                age=30,
                gender="male",
                goal="unknown_goal"
            )
        
        # 无效饮食限制
        with pytest.raises(ValueError):
            NutritionPlannerArguments(
                height=170,
                weight=70,
                age=30,
                gender="male",
                dietary_restrictions=["unknown_restriction"]
            )
        
        # 无效语言
        with pytest.raises(ValueError):
            NutritionPlannerArguments(
                height=170,
                weight=70,
                age=30,
                gender="male",
                language="fr"
            )
    
    @pytest.mark.asyncio
    async def test_target_weight_validation(self, prompt):
        """测试目标体重验证"""
        # 目标体重过度不合理的情况
        args = NutritionPlannerArguments(
            height=170,
            weight=70,
            age=30,
            gender="male",
            target_weight=150  # 差异过大
        )
        
        result = await prompt.generate(args)
        assert result.success is False
        assert "参数验证失败" in result.error_message
    
    @pytest.mark.asyncio
    async def test_comprehensive_planning(self, prompt):
        """测试综合配餐方案"""
        args = NutritionPlannerArguments(
            height=172,
            weight=68,
            age=32,
            gender="female",
            activity_level="moderately_active",
            goal="lose_weight",
            target_weight=63,
            timeline_weeks=16,
            dietary_restrictions=["vegetarian"],
            meals_per_day=4,
            language="zh"
        )
        
        result = await prompt.generate(args)
        
        assert result.success is True
        
        # 验证包含所有必要的计算内容
        content = result.content
        assert "BMR" in content or "基础代谢率" in content
        assert "TDEE" in content or "总热量消耗" in content
        assert "蛋白质" in content
        assert "碳水化合物" in content  
        assert "脂肪" in content
        assert "素食" in content or "vegetarian" in content.lower()
        assert "减重" in content or "减肥" in content
        assert "4餐" in content or "四餐" in content
        
        # 验证元数据完整性
        metadata = result.metadata
        assert metadata["height"] == 172
        assert metadata["weight"] == 68
        assert metadata["target_weight"] == 63
        assert metadata["timeline_weeks"] == 16
        assert metadata["dietary_restrictions"] == ["vegetarian"]
        assert metadata["meals_per_day"] == 4
    
    @pytest.mark.asyncio
    async def test_special_dietary_restrictions(self, prompt):
        """测试特殊饮食限制"""
        special_restrictions = [
            ["vegan"],
            ["diabetic"], 
            ["keto"],
            ["gluten_free", "dairy_free"],
            ["low_sodium", "diabetic"]
        ]
        
        for restrictions in special_restrictions:
            args = NutritionPlannerArguments(
                height=170,
                weight=70,
                age=40,
                gender="male",
                dietary_restrictions=restrictions
            )
            
            result = await prompt.generate(args)
            
            assert result.success is True
            assert result.metadata["dietary_restrictions"] == restrictions
    
    @pytest.mark.asyncio
    async def test_different_demographics(self, prompt):
        """测试不同人群"""
        demographics = [
            {"age": 18, "gender": "female", "goal": "gain_weight"},
            {"age": 25, "gender": "male", "goal": "gain_muscle"},
            {"age": 45, "gender": "female", "goal": "lose_weight"},
            {"age": 60, "gender": "male", "goal": "maintain"},
            {"age": 70, "gender": "female", "goal": "maintain"}
        ]
        
        for demo in demographics:
            args = NutritionPlannerArguments(
                height=170,
                weight=70,
                **demo
            )
            
            result = await prompt.generate(args)
            
            assert result.success is True
            assert result.metadata["age"] == demo["age"]
            assert result.metadata["gender"] == demo["gender"]
            assert result.metadata["goal"] == demo["goal"]
    
    def test_activity_multiplier(self, prompt):
        """测试活动水平系数"""
        assert prompt._get_activity_multiplier("sedentary") == 1.2
        assert prompt._get_activity_multiplier("lightly_active") == 1.375
        assert prompt._get_activity_multiplier("moderately_active") == 1.55
        assert prompt._get_activity_multiplier("very_active") == 1.725
        assert prompt._get_activity_multiplier("extra_active") == 1.9
        assert prompt._get_activity_multiplier("unknown") == 1.55  # 默认值
    
    def test_goal_descriptions(self, prompt):
        """测试目标描述"""
        # 中文描述
        assert "维持" in prompt._get_goal_description_zh("maintain")
        assert "减重" in prompt._get_goal_description_zh("lose_weight")
        assert "增重" in prompt._get_goal_description_zh("gain_weight")
        assert "增肌" in prompt._get_goal_description_zh("gain_muscle")
        
        # 英文描述
        assert "Maintain" in prompt._get_goal_description_en("maintain")
        assert "loss" in prompt._get_goal_description_en("lose_weight")
        assert "gain" in prompt._get_goal_description_en("gain_weight")
        assert "building" in prompt._get_goal_description_en("gain_muscle")
    
    def test_dietary_restrictions_text(self, prompt):
        """测试饮食限制文本"""
        restrictions = ["vegetarian", "gluten_free"]
        
        # 中文
        zh_text = prompt._get_dietary_restrictions_text_zh(restrictions)
        assert "素食" in zh_text
        assert "无麸质" in zh_text
        
        # 英文
        en_text = prompt._get_dietary_restrictions_text_en(restrictions)
        assert "Vegetarian" in en_text
        assert "Gluten-free" in en_text