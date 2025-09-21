"""
营养配餐计算器Prompt实现
生成指导Claude计算营养需求、制定配餐方案的文本
"""
from typing import Type, Optional, List
from pydantic import BaseModel, Field, field_validator
from .base_prompt import BasePrompt
from ..base.models import PromptResult


class NutritionPlannerArguments(BaseModel):
    """营养配餐参数模型"""
    height: float = Field(..., description="身高（厘米）", gt=100, le=250)
    weight: float = Field(..., description="体重（公斤）", gt=30, le=200)
    age: int = Field(..., description="年龄", ge=1, le=120)
    gender: str = Field(..., description="性别: male(男) 或 female(女)")
    activity_level: str = Field(
        "moderately_active",
        description="活动水平: sedentary(久坐), lightly_active(轻度), moderately_active(中度), very_active(高度), extra_active(极高)"
    )
    goal: str = Field(
        "maintain",
        description="饮食目标: maintain(维持), lose_weight(减重), gain_weight(增重), gain_muscle(增肌)"
    )
    dietary_restrictions: Optional[List[str]] = Field(
        None,
        description="饮食限制: vegetarian(素食), vegan(纯素), gluten_free(无麸质), dairy_free(无乳制品), low_sodium(低钠), diabetic(糖尿病饮食)"
    )
    target_weight: Optional[float] = Field(
        None,
        description="目标体重（公斤，用于减重/增重计划）",
        gt=30,
        le=200
    )
    timeline_weeks: Optional[int] = Field(
        None,
        description="时间目标（多少周内达到目标）",
        ge=1,
        le=104
    )
    meals_per_day: int = Field(
        3,
        description="每日餐次数量（包括正餐和加餐）",
        ge=3,
        le=6
    )
    language: str = Field("zh", description="输出语言: zh(中文) 或 en(英文)")
    
    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if v not in ['male', 'female']:
            raise ValueError('性别必须是 "male" 或 "female"')
        return v
    
    @field_validator('activity_level')
    @classmethod
    def validate_activity_level(cls, v):
        valid_levels = ['sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extra_active']
        if v not in valid_levels:
            raise ValueError(f'活动水平必须是以下之一: {", ".join(valid_levels)}')
        return v
    
    @field_validator('goal')
    @classmethod
    def validate_goal(cls, v):
        valid_goals = ['maintain', 'lose_weight', 'gain_weight', 'gain_muscle']
        if v not in valid_goals:
            raise ValueError(f'饮食目标必须是以下之一: {", ".join(valid_goals)}')
        return v
    
    @field_validator('dietary_restrictions')
    @classmethod
    def validate_dietary_restrictions(cls, v):
        if v is not None:
            valid_restrictions = [
                'vegetarian', 'vegan', 'gluten_free', 'dairy_free', 
                'low_sodium', 'diabetic', 'keto', 'paleo'
            ]
            for restriction in v:
                if restriction not in valid_restrictions:
                    raise ValueError(f'饮食限制必须是以下之一: {", ".join(valid_restrictions)}')
        return v
    
    @field_validator('language')
    @classmethod
    def validate_language(cls, v):
        if v not in ['zh', 'en']:
            raise ValueError('语言必须是 "zh" 或 "en"')
        return v


class NutritionPlannerPrompt(BasePrompt):
    """营养配餐计算器Prompt实现"""
    
    @property
    def name(self) -> str:
        return "nutrition_planner"
    
    @property
    def description(self) -> str:
        return "智能营养配餐计算器，根据个人情况计算营养需求，制定科学的饮食计划和配餐方案"
    
    @property
    def arguments_schema(self) -> Type[BaseModel]:
        return NutritionPlannerArguments
    
    def validate_arguments(self, arguments: NutritionPlannerArguments) -> bool:
        """验证参数有效性"""
        try:
            # 检查身高体重的合理性
            if not (100 <= arguments.height <= 250):
                return False
            if not (30 <= arguments.weight <= 200):
                return False
            
            # 如果有目标体重，检查其合理性
            if arguments.target_weight:
                if not (30 <= arguments.target_weight <= 200):
                    return False
                # 目标体重不应与当前体重相差过大
                weight_diff = abs(arguments.target_weight - arguments.weight)
                if weight_diff > 50:  # 最大差异50公斤
                    return False
            
            # 如果有时间目标，检查合理性
            if arguments.timeline_weeks:
                if not (1 <= arguments.timeline_weeks <= 104):  # 最多2年
                    return False
            
            return True
        except Exception:
            return False
    
    async def generate(self, arguments: NutritionPlannerArguments) -> PromptResult:
        """生成营养配餐计算Prompt文本"""
        if not self.validate_arguments(arguments):
            return PromptResult(
                success=False,
                content="",
                error_message="参数验证失败：请检查身高、体重、目标体重等参数是否在合理范围内",
                prompt_name=self.name
            )
        
        try:
            # 生成引导Claude计算营养配餐的prompt文本
            if arguments.language == "zh":
                prompt_content = self._generate_chinese_prompt(arguments)
            else:
                prompt_content = self._generate_english_prompt(arguments)
            
            # 准备元数据
            metadata = {
                "height": arguments.height,
                "weight": arguments.weight,
                "age": arguments.age,
                "gender": arguments.gender,
                "activity_level": arguments.activity_level,
                "goal": arguments.goal,
                "meals_per_day": arguments.meals_per_day,
                "language": arguments.language
            }
            
            if arguments.target_weight:
                metadata["target_weight"] = arguments.target_weight
            if arguments.timeline_weeks:
                metadata["timeline_weeks"] = arguments.timeline_weeks
            if arguments.dietary_restrictions:
                metadata["dietary_restrictions"] = arguments.dietary_restrictions
            
            return PromptResult(
                success=True,
                content=prompt_content,
                prompt_name=self.name,
                metadata=metadata
            )
            
        except Exception as e:
            return PromptResult(
                success=False,
                content="",
                error_message=f"生成营养配餐Prompt失败: {str(e)}",
                prompt_name=self.name
            )
    
    def _get_activity_multiplier(self, level: str) -> float:
        """获取活动水平系数"""
        multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extra_active': 1.9
        }
        return multipliers.get(level, 1.55)
    
    def _get_goal_description_zh(self, goal: str) -> str:
        """获取饮食目标的中文描述"""
        descriptions = {
            'maintain': '维持当前体重',
            'lose_weight': '健康减重',
            'gain_weight': '健康增重',
            'gain_muscle': '增肌塑形'
        }
        return descriptions.get(goal, '维持当前体重')
    
    def _get_goal_description_en(self, goal: str) -> str:
        """获取饮食目标的英文描述"""
        descriptions = {
            'maintain': 'Maintain current weight',
            'lose_weight': 'Healthy weight loss',
            'gain_weight': 'Healthy weight gain',
            'gain_muscle': 'Muscle building'
        }
        return descriptions.get(goal, 'Maintain current weight')
    
    def _get_dietary_restrictions_text_zh(self, restrictions: List[str]) -> str:
        """获取饮食限制的中文描述"""
        restriction_map = {
            'vegetarian': '素食主义',
            'vegan': '纯素食主义',
            'gluten_free': '无麸质饮食',
            'dairy_free': '无乳制品饮食',
            'low_sodium': '低钠饮食',
            'diabetic': '糖尿病饮食',
            'keto': '生酮饮食',
            'paleo': '原始人饮食'
        }
        return '、'.join([restriction_map.get(r, r) for r in restrictions])
    
    def _get_dietary_restrictions_text_en(self, restrictions: List[str]) -> str:
        """获取饮食限制的英文描述"""
        restriction_map = {
            'vegetarian': 'Vegetarian',
            'vegan': 'Vegan',
            'gluten_free': 'Gluten-free',
            'dairy_free': 'Dairy-free',
            'low_sodium': 'Low sodium',
            'diabetic': 'Diabetic diet',
            'keto': 'Ketogenic',
            'paleo': 'Paleo'
        }
        return ', '.join([restriction_map.get(r, r) for r in restrictions])
    
    def _generate_chinese_prompt(self, args: NutritionPlannerArguments) -> str:
        """生成中文指导prompt"""
        gender_text = "男性" if args.gender == "male" else "女性"
        goal_text = self._get_goal_description_zh(args.goal)
        
        prompt = f"""请帮我制定专业的营养配餐方案，基于以下信息：

## 📋 基本信息
- 身高：{args.height} 厘米
- 体重：{args.weight} 公斤
- 年龄：{args.age} 岁
- 性别：{gender_text}
- 活动水平：{self._get_activity_level_description_zh(args.activity_level)}
- 饮食目标：{goal_text}
- 每日餐次：{args.meals_per_day} 餐"""
        
        if args.target_weight:
            prompt += f"\n- 目标体重：{args.target_weight} 公斤"
        
        if args.timeline_weeks:
            prompt += f"\n- 时间目标：{args.timeline_weeks} 周"
        
        if args.dietary_restrictions:
            restrictions_text = self._get_dietary_restrictions_text_zh(args.dietary_restrictions)
            prompt += f"\n- 饮食限制：{restrictions_text}"
        
        prompt += """

请使用calculator-mcp的数学运算工具完成以下计算和分析：

## 🔢 第一步：基础代谢和热量需求计算

1. **计算基础代谢率（BMR）**
   使用Mifflin-St Jeor公式："""
        
        if args.gender == "male":
            prompt += f"""
   男性公式：BMR = (10 × {args.weight}) + (6.25 × {args.height}) - (5 × {args.age}) + 5"""
        else:
            prompt += f"""
   女性公式：BMR = (10 × {args.weight}) + (6.25 × {args.height}) - (5 × {args.age}) - 161"""
        
        activity_multiplier = self._get_activity_multiplier(args.activity_level)
        prompt += f"""
   - 使用multiplication和addition/subtraction工具计算

2. **计算每日总热量消耗（TDEE）**
   - TDEE = BMR × {activity_multiplier} （活动系数）
   - 使用multiplication工具计算

3. **根据目标调整热量摄入**"""
        
        if args.goal == "lose_weight":
            prompt += """
   减重目标：目标热量 = TDEE - 300到500千卡（每周减重0.3-0.5公斤）"""
        elif args.goal == "gain_weight":
            prompt += """
   增重目标：目标热量 = TDEE + 300到500千卡（每周增重0.3-0.5公斤）"""
        elif args.goal == "gain_muscle":
            prompt += """
   增肌目标：目标热量 = TDEE + 200到400千卡（支持肌肉合成）"""
        else:
            prompt += """
   维持体重：目标热量 = TDEE ± 50千卡"""
        
        prompt += """

## 🥗 第二步：营养素分配计算

请根据饮食目标计算三大营养素分配：

4. **蛋白质需求计算**"""
        
        if args.goal == "gain_muscle":
            prompt += f"""
   增肌期：{args.weight} × 2.0克/公斤 = [使用multiplication计算] 克/天"""
        elif args.goal == "lose_weight":
            prompt += f"""
   减重期：{args.weight} × 1.6克/公斤 = [使用multiplication计算] 克/天"""
        else:
            prompt += f"""
   一般需求：{args.weight} × 1.2克/公斤 = [使用multiplication计算] 克/天"""
        
        prompt += """
   - 蛋白质热量：蛋白质克数 × 4千卡/克

5. **脂肪需求计算**
   - 脂肪热量：目标总热量 × 25-30%
   - 脂肪克数：脂肪热量 ÷ 9千卡/克

6. **碳水化合物需求计算**
   - 碳水热量：目标总热量 - 蛋白质热量 - 脂肪热量
   - 碳水克数：碳水热量 ÷ 4千卡/克

## 🍽️ 第三步：餐次分配计算

7. **计算各餐热量分配**"""
        
        if args.meals_per_day == 3:
            prompt += """
   三餐分配：
   - 早餐：总热量 × 25-30%
   - 午餐：总热量 × 35-40%
   - 晚餐：总热量 × 30-35%"""
        elif args.meals_per_day == 4:
            prompt += """
   四餐分配：
   - 早餐：总热量 × 25%
   - 午餐：总热量 × 30%
   - 晚餐：总热量 × 30%
   - 加餐：总热量 × 15%"""
        else:
            prompt += f"""
   {args.meals_per_day}餐分配：请均匀分配总热量，主餐占比更高"""
        
        if args.dietary_restrictions:
            prompt += f"""

## 🚫 饮食限制考虑

特殊饮食要求：{self._get_dietary_restrictions_text_zh(args.dietary_restrictions)}
请在食物推荐中严格遵守这些限制，并提供替代食物建议。"""
        
        prompt += """

## 📊 输出格式要求

请按以下格式输出完整的营养配餐方案：

### 🧮 营养需求计算结果

#### 基础数据
- 基础代谢率（BMR）：[计算结果] 千卡/天
- 总热量消耗（TDEE）：[计算结果] 千卡/天
- 目标热量摄入：[计算结果] 千卡/天

#### 营养素分配
- 蛋白质：[X] 克/天（[Y] 千卡，占总热量 [Z]%）
- 碳水化合物：[X] 克/天（[Y] 千卡，占总热量 [Z]%）
- 脂肪：[X] 克/天（[Y] 千卡，占总热量 [Z]%）

### 🍽️ 每日配餐方案

#### 餐次热量分配"""
        
        for i in range(1, args.meals_per_day + 1):
            meal_names = ["早餐", "午餐", "晚餐", "上午加餐", "下午加餐", "晚间加餐"]
            meal_name = meal_names[i-1] if i <= len(meal_names) else f"第{i}餐"
            prompt += f"""
- {meal_name}：[X] 千卡（蛋白质 [Y]g，碳水 [Z]g，脂肪 [W]g）"""
        
        prompt += """

### 🥘 食物类别推荐

#### 优质蛋白质来源
- 动物蛋白：[具体推荐和份量]
- 植物蛋白：[具体推荐和份量]

#### 复合碳水化合物来源
- 全谷物：[具体推荐和份量]
- 蔬菜：[具体推荐和份量]
- 水果：[具体推荐和份量]

#### 健康脂肪来源
- 坚果类：[具体推荐和份量]
- 优质油脂：[具体推荐和份量]

### 💡 个性化营养建议

1. **饮食时间安排**：[具体建议]
2. **水分摄入**：[每日饮水量建议]
3. **维生素矿物质**：[重点关注的营养素]
4. **饮食注意事项**：[根据目标和限制的特殊提醒]
5. **进度监测**：[如何评估饮食效果]

### ⚠️ 重要提醒

- 本方案为一般性营养建议，个体差异较大
- 特殊健康状况请咨询专业营养师或医生
- 建议定期调整方案以适应身体变化
- 配合适量运动以达到最佳效果

请确保所有计算都使用calculator-mcp的数学工具完成，保证计算的准确性。"""
        
        return prompt
    
    def _get_activity_level_description_zh(self, level: str) -> str:
        """获取活动水平的中文描述"""
        descriptions = {
            'sedentary': '久坐（很少运动）',
            'lightly_active': '轻度活动（每周运动1-3天）',
            'moderately_active': '中度活动（每周运动3-5天）',
            'very_active': '高度活动（每周运动6-7天）',
            'extra_active': '极高活动（每天高强度运动）'
        }
        return descriptions.get(level, '中度活动')
    
    def _generate_english_prompt(self, args: NutritionPlannerArguments) -> str:
        """生成英文指导prompt"""
        goal_text = self._get_goal_description_en(args.goal)
        
        prompt = f"""Please help me create a professional nutrition and meal planning solution based on the following information:

## 📋 Basic Information
- Height: {args.height} cm
- Weight: {args.weight} kg
- Age: {args.age} years
- Gender: {args.gender}
- Activity Level: {self._get_activity_level_description_en(args.activity_level)}
- Dietary Goal: {goal_text}
- Meals per Day: {args.meals_per_day} meals"""
        
        if args.target_weight:
            prompt += f"\n- Target Weight: {args.target_weight} kg"
        
        if args.timeline_weeks:
            prompt += f"\n- Timeline: {args.timeline_weeks} weeks"
        
        if args.dietary_restrictions:
            restrictions_text = self._get_dietary_restrictions_text_en(args.dietary_restrictions)
            prompt += f"\n- Dietary Restrictions: {restrictions_text}"
        
        prompt += """

Please use calculator-mcp mathematical tools to complete the following calculations and analysis:

## 🔢 Step 1: Basal Metabolic Rate and Calorie Requirements

1. **Calculate Basal Metabolic Rate (BMR)**
   Using Mifflin-St Jeor formula:"""
        
        if args.gender == "male":
            prompt += f"""
   Male formula: BMR = (10 × {args.weight}) + (6.25 × {args.height}) - (5 × {args.age}) + 5"""
        else:
            prompt += f"""
   Female formula: BMR = (10 × {args.weight}) + (6.25 × {args.height}) - (5 × {args.age}) - 161"""
        
        activity_multiplier = self._get_activity_multiplier(args.activity_level)
        prompt += f"""
   - Use multiplication and addition/subtraction tools

2. **Calculate Total Daily Energy Expenditure (TDEE)**
   - TDEE = BMR × {activity_multiplier} (activity factor)
   - Use multiplication tool

3. **Adjust calorie intake based on goal**"""
        
        if args.goal == "lose_weight":
            prompt += """
   Weight loss goal: Target calories = TDEE - 300 to 500 kcal (0.3-0.5 kg loss per week)"""
        elif args.goal == "gain_weight":
            prompt += """
   Weight gain goal: Target calories = TDEE + 300 to 500 kcal (0.3-0.5 kg gain per week)"""
        elif args.goal == "gain_muscle":
            prompt += """
   Muscle building goal: Target calories = TDEE + 200 to 400 kcal (support muscle synthesis)"""
        else:
            prompt += """
   Weight maintenance: Target calories = TDEE ± 50 kcal"""
        
        prompt += """

## 🥗 Step 2: Macronutrient Distribution

Calculate macronutrient distribution based on dietary goal:

4. **Protein Requirements**"""
        
        if args.goal == "gain_muscle":
            prompt += f"""
   Muscle building: {args.weight} × 2.0g/kg = [use multiplication] g/day"""
        elif args.goal == "lose_weight":
            prompt += f"""
   Weight loss: {args.weight} × 1.6g/kg = [use multiplication] g/day"""
        else:
            prompt += f"""
   General needs: {args.weight} × 1.2g/kg = [use multiplication] g/day"""
        
        prompt += """
   - Protein calories: protein grams × 4 kcal/g

5. **Fat Requirements**
   - Fat calories: target total calories × 25-30%
   - Fat grams: fat calories ÷ 9 kcal/g

6. **Carbohydrate Requirements**
   - Carb calories: target total calories - protein calories - fat calories
   - Carb grams: carb calories ÷ 4 kcal/g

## 🍽️ Step 3: Meal Distribution

7. **Calculate meal calorie distribution**"""
        
        if args.meals_per_day == 3:
            prompt += """
   Three meals:
   - Breakfast: total calories × 25-30%
   - Lunch: total calories × 35-40%
   - Dinner: total calories × 30-35%"""
        elif args.meals_per_day == 4:
            prompt += """
   Four meals:
   - Breakfast: total calories × 25%
   - Lunch: total calories × 30%
   - Dinner: total calories × 30%
   - Snack: total calories × 15%"""
        else:
            prompt += f"""
   {args.meals_per_day} meals: distribute total calories evenly, with main meals having higher proportions"""
        
        if args.dietary_restrictions:
            prompt += f"""

## 🚫 Dietary Restrictions

Special dietary requirements: {self._get_dietary_restrictions_text_en(args.dietary_restrictions)}
Please strictly adhere to these restrictions in food recommendations and provide alternative food suggestions."""
        
        prompt += """

## 📊 Required Output Format

Please output the complete nutrition and meal plan in the following format:

### 🧮 Nutrition Requirements Calculation Results

#### Basic Data
- Basal Metabolic Rate (BMR): [result] kcal/day
- Total Daily Energy Expenditure (TDEE): [result] kcal/day
- Target calorie intake: [result] kcal/day

#### Macronutrient Distribution
- Protein: [X] g/day ([Y] kcal, [Z]% of total calories)
- Carbohydrates: [X] g/day ([Y] kcal, [Z]% of total calories)
- Fat: [X] g/day ([Y] kcal, [Z]% of total calories)

### 🍽️ Daily Meal Plan

#### Meal Calorie Distribution"""
        
        meal_names = ["Breakfast", "Lunch", "Dinner", "Morning Snack", "Afternoon Snack", "Evening Snack"]
        for i in range(1, args.meals_per_day + 1):
            meal_name = meal_names[i-1] if i <= len(meal_names) else f"Meal {i}"
            prompt += f"""
- {meal_name}: [X] kcal (Protein [Y]g, Carbs [Z]g, Fat [W]g)"""
        
        prompt += """

### 🥘 Food Category Recommendations

#### Quality Protein Sources
- Animal protein: [specific recommendations and portions]
- Plant protein: [specific recommendations and portions]

#### Complex Carbohydrate Sources
- Whole grains: [specific recommendations and portions]
- Vegetables: [specific recommendations and portions]
- Fruits: [specific recommendations and portions]

#### Healthy Fat Sources
- Nuts and seeds: [specific recommendations and portions]
- Quality oils: [specific recommendations and portions]

### 💡 Personalized Nutrition Advice

1. **Meal Timing**: [specific recommendations]
2. **Hydration**: [daily water intake recommendations]
3. **Vitamins and Minerals**: [key nutrients to focus on]
4. **Dietary Considerations**: [special reminders based on goals and restrictions]
5. **Progress Monitoring**: [how to evaluate dietary effectiveness]

### ⚠️ Important Reminders

- This plan provides general nutrition advice; individual differences vary significantly
- Consult a professional nutritionist or doctor for special health conditions
- Regularly adjust the plan to adapt to body changes
- Combine with appropriate exercise for optimal results

Please ensure all calculations are completed using calculator-mcp mathematical tools to guarantee accuracy."""
        
        return prompt
    
    def _get_activity_level_description_en(self, level: str) -> str:
        """获取活动水平的英文描述"""
        descriptions = {
            'sedentary': 'Sedentary (little exercise)',
            'lightly_active': 'Lightly active (exercise 1-3 days/week)',
            'moderately_active': 'Moderately active (exercise 3-5 days/week)',
            'very_active': 'Very active (exercise 6-7 days/week)',
            'extra_active': 'Extra active (very hard exercise daily)'
        }
        return descriptions.get(level, 'Moderately active')