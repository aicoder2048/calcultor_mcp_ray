"""
BMI与健康指标计算器Prompt实现
生成指导Claude计算BMI、基础代谢率、每日热量需求等健康指标的文本
"""
from typing import Type, Optional
from pydantic import BaseModel, Field, field_validator
from .base_prompt import BasePrompt
from ..base.models import PromptResult


class HealthMetricsArguments(BaseModel):
    """健康指标参数模型"""
    height: float = Field(..., description="身高（厘米或英寸）", gt=0, le=300)
    weight: float = Field(..., description="体重（公斤或磅）", gt=0, le=2500)
    age: Optional[int] = Field(None, description="年龄（用于BMR计算）", ge=1, le=120)
    gender: Optional[str] = Field(None, description="性别: male(男) 或 female(女)")
    activity_level: Optional[str] = Field(
        "sedentary", 
        description="活动水平: sedentary(久坐), lightly_active(轻度活动), moderately_active(中度活动), very_active(高度活动), extra_active(极高活动)"
    )
    unit_system: str = Field("metric", description="单位制: metric(公制) 或 imperial(英制)")
    language: str = Field("zh", description="输出语言: zh(中文) 或 en(英文)")
    
    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if v is not None and v not in ['male', 'female']:
            raise ValueError('性别必须是 "male" 或 "female"')
        return v
    
    @field_validator('activity_level')
    @classmethod
    def validate_activity_level(cls, v):
        valid_levels = ['sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extra_active']
        if v not in valid_levels:
            raise ValueError(f'活动水平必须是以下之一: {", ".join(valid_levels)}')
        return v
    
    @field_validator('unit_system')
    @classmethod
    def validate_unit_system(cls, v):
        if v not in ['metric', 'imperial']:
            raise ValueError('单位制必须是 "metric" 或 "imperial"')
        return v
    
    @field_validator('language')
    @classmethod
    def validate_language(cls, v):
        if v not in ['zh', 'en']:
            raise ValueError('语言必须是 "zh" 或 "en"')
        return v


class HealthMetricsPrompt(BasePrompt):
    """BMI与健康指标计算器Prompt实现"""
    
    @property
    def name(self) -> str:
        return "health_metrics"
    
    @property
    def description(self) -> str:
        return "计算BMI、基础代谢率、每日热量需求等健康指标，提供个性化健康建议"
    
    @property
    def arguments_schema(self) -> Type[BaseModel]:
        return HealthMetricsArguments
    
    def validate_arguments(self, arguments: HealthMetricsArguments) -> bool:
        """验证参数有效性"""
        try:
            # 检查身高体重的合理范围
            if arguments.unit_system == "metric":
                # 公制：身高30-300厘米，体重1-1000公斤
                if not (30 <= arguments.height <= 300):
                    return False
                if not (1 <= arguments.weight <= 1000):
                    return False
            else:
                # 英制：身高12-120英寸，体重2-2500磅
                if not (12 <= arguments.height <= 120):
                    return False
                if not (2 <= arguments.weight <= 2500):
                    return False
            
            return True
        except Exception:
            return False
    
    async def generate(self, arguments: HealthMetricsArguments) -> PromptResult:
        """生成健康指标计算Prompt文本"""
        if not self.validate_arguments(arguments):
            return PromptResult(
                success=False,
                content="",
                error_message="参数验证失败：请检查身高体重是否在合理范围内",
                prompt_name=self.name
            )
        
        try:
            # 生成引导Claude计算健康指标的prompt文本
            if arguments.language == "zh":
                prompt_content = self._generate_chinese_prompt(arguments)
            else:
                prompt_content = self._generate_english_prompt(arguments)
            
            # 准备元数据
            metadata = {
                "height": arguments.height,
                "weight": arguments.weight,
                "unit_system": arguments.unit_system,
                "language": arguments.language
            }
            if arguments.age:
                metadata["age"] = arguments.age
            if arguments.gender:
                metadata["gender"] = arguments.gender
            if arguments.activity_level:
                metadata["activity_level"] = arguments.activity_level
            
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
                error_message=f"生成健康指标Prompt失败: {str(e)}",
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
        return multipliers.get(level, 1.2)
    
    def _get_activity_description_zh(self, level: str) -> str:
        """获取活动水平的中文描述"""
        descriptions = {
            'sedentary': '久坐（很少或没有运动）',
            'lightly_active': '轻度活动（每周运动1-3天）',
            'moderately_active': '中度活动（每周运动3-5天）',
            'very_active': '高度活动（每周运动6-7天）',
            'extra_active': '极高活动（每天高强度运动或体力工作）'
        }
        return descriptions.get(level, '久坐')
    
    def _get_activity_description_en(self, level: str) -> str:
        """获取活动水平的英文描述"""
        descriptions = {
            'sedentary': 'Sedentary (little or no exercise)',
            'lightly_active': 'Lightly active (exercise 1-3 days/week)',
            'moderately_active': 'Moderately active (exercise 3-5 days/week)',
            'very_active': 'Very active (exercise 6-7 days/week)',
            'extra_active': 'Extra active (very hard exercise daily or physical job)'
        }
        return descriptions.get(level, 'Sedentary')
    
    def _generate_chinese_prompt(self, args: HealthMetricsArguments) -> str:
        """生成中文指导prompt"""
        unit_info = "公制单位" if args.unit_system == "metric" else "英制单位"
        height_unit = "厘米" if args.unit_system == "metric" else "英寸"
        weight_unit = "公斤" if args.unit_system == "metric" else "磅"
        
        prompt = f"""请帮我计算和分析健康指标，基于以下信息：

基本信息：
- 身高：{args.height} {height_unit}
- 体重：{args.weight} {weight_unit}
- 单位制：{unit_info}
"""
        
        if args.age:
            prompt += f"- 年龄：{args.age} 岁\n"
        if args.gender:
            gender_text = "男性" if args.gender == "male" else "女性"
            prompt += f"- 性别：{gender_text}\n"
        if args.activity_level:
            prompt += f"- 活动水平：{self._get_activity_description_zh(args.activity_level)}\n"
        
        prompt += """
请使用calculator-mcp的数学运算工具完成以下计算和分析：

1. **BMI（身体质量指数）计算**
   - 使用division工具计算：体重(kg) ÷ 身高²(m²)
"""
        
        if args.unit_system == "imperial":
            prompt += """   - 首先将英制单位转换为公制：
     * 体重：磅 × 0.453592 = 公斤
     * 身高：英寸 × 0.0254 = 米
"""
        else:
            prompt += """   - 将身高从厘米转换为米：身高 ÷ 100
"""
        
        prompt += """   - 使用square工具计算身高的平方
   - 使用division工具计算最终BMI值

2. **BMI健康状态评估**
   根据WHO标准分类：
   - BMI < 18.5：体重过轻
   - 18.5 ≤ BMI < 24：正常体重
   - 24 ≤ BMI < 28：超重
   - 28 ≤ BMI < 30：肥胖I级（轻度）
   - 30 ≤ BMI < 35：肥胖II级（中度）
   - BMI ≥ 35：肥胖III级（重度）

3. **理想体重范围计算**
   - 最小理想体重：使用multiplication工具计算 18.5 × 身高²(m²)
   - 最大理想体重：使用multiplication工具计算 24 × 身高²(m²)
"""
        
        if args.age and args.gender:
            prompt += f"""
4. **基础代谢率（BMR）计算**
   使用Mifflin-St Jeor公式：
"""
            if args.gender == "male":
                prompt += """   男性：BMR = (10 × 体重kg) + (6.25 × 身高cm) - (5 × 年龄) + 5
"""
            else:
                prompt += """   女性：BMR = (10 × 体重kg) + (6.25 × 身高cm) - (5 × 年龄) - 161
"""
            prompt += """   - 使用multiplication和addition/subtraction工具进行计算
"""
            
            if args.activity_level:
                multiplier = self._get_activity_multiplier(args.activity_level)
                prompt += f"""
5. **每日热量需求（TDEE）计算**
   - TDEE = BMR × {multiplier} （{self._get_activity_description_zh(args.activity_level)}）
   - 使用multiplication工具计算
"""
        
        prompt += """
请按以下格式输出结果：

### 🏥 健康指标分析报告

#### 📊 基本测量值
- 身高：[值] [单位]
- 体重：[值] [单位]

#### 💪 BMI分析
- BMI值：[计算结果]
- 健康状态：[分类]
- 评估：[根据BMI值给出健康评估]

#### ⚖️ 理想体重范围
- 建议体重范围：[最小值] - [最大值] [单位]
- 当前差异：[与理想范围的差异]
"""
        
        if args.age and args.gender:
            prompt += """
#### 🔥 代谢率分析
- 基础代谢率（BMR）：[值] 千卡/天
- 说明：这是您在完全休息状态下维持基本生理功能所需的热量
"""
            if args.activity_level:
                prompt += """- 每日热量需求（TDEE）：[值] 千卡/天
- 活动水平：[描述]
- 建议：[基于TDEE给出的饮食和运动建议]
"""
        
        prompt += """
#### 💡 健康建议
[基于计算结果提供3-5条个性化健康建议]

请确保所有计算都使用calculator-mcp的工具完成，保证计算的准确性。"""
        
        return prompt
    
    def _generate_english_prompt(self, args: HealthMetricsArguments) -> str:
        """生成英文指导prompt"""
        unit_info = "metric units" if args.unit_system == "metric" else "imperial units"
        height_unit = "cm" if args.unit_system == "metric" else "inches"
        weight_unit = "kg" if args.unit_system == "metric" else "lbs"
        
        prompt = f"""Please calculate and analyze health metrics based on the following information:

Basic Information:
- Height: {args.height} {height_unit}
- Weight: {args.weight} {weight_unit}
- Unit System: {unit_info}
"""
        
        if args.age:
            prompt += f"- Age: {args.age} years\n"
        if args.gender:
            prompt += f"- Gender: {args.gender}\n"
        if args.activity_level:
            prompt += f"- Activity Level: {self._get_activity_description_en(args.activity_level)}\n"
        
        prompt += """
Please use calculator-mcp mathematical tools to complete the following calculations and analysis:

1. **BMI (Body Mass Index) Calculation**
   - Use division tool to calculate: weight(kg) ÷ height²(m²)
"""
        
        if args.unit_system == "imperial":
            prompt += """   - First convert imperial units to metric:
     * Weight: pounds × 0.453592 = kilograms
     * Height: inches × 0.0254 = meters
"""
        else:
            prompt += """   - Convert height from centimeters to meters: height ÷ 100
"""
        
        prompt += """   - Use square tool to calculate height squared
   - Use division tool to calculate final BMI value

2. **BMI Health Status Assessment**
   According to WHO standards:
   - BMI < 18.5: Underweight
   - 18.5 ≤ BMI < 25: Normal weight
   - 25 ≤ BMI < 30: Overweight
   - 30 ≤ BMI < 35: Obese Class I (Mild)
   - 35 ≤ BMI < 40: Obese Class II (Moderate)
   - BMI ≥ 40: Obese Class III (Severe)

3. **Ideal Weight Range Calculation**
   - Minimum ideal weight: Use multiplication tool to calculate 18.5 × height²(m²)
   - Maximum ideal weight: Use multiplication tool to calculate 24.9 × height²(m²)
"""
        
        if args.age and args.gender:
            prompt += f"""
4. **Basal Metabolic Rate (BMR) Calculation**
   Using Mifflin-St Jeor formula:
"""
            if args.gender == "male":
                prompt += """   Male: BMR = (10 × weight kg) + (6.25 × height cm) - (5 × age) + 5
"""
            else:
                prompt += """   Female: BMR = (10 × weight kg) + (6.25 × height cm) - (5 × age) - 161
"""
            prompt += """   - Use multiplication and addition/subtraction tools for calculation
"""
            
            if args.activity_level:
                multiplier = self._get_activity_multiplier(args.activity_level)
                prompt += f"""
5. **Total Daily Energy Expenditure (TDEE) Calculation**
   - TDEE = BMR × {multiplier} ({self._get_activity_description_en(args.activity_level)})
   - Use multiplication tool to calculate
"""
        
        prompt += """
Please output results in the following format:

### 🏥 Health Metrics Analysis Report

#### 📊 Basic Measurements
- Height: [value] [unit]
- Weight: [value] [unit]

#### 💪 BMI Analysis
- BMI Value: [calculated result]
- Health Status: [classification]
- Assessment: [health assessment based on BMI value]

#### ⚖️ Ideal Weight Range
- Recommended Weight Range: [min value] - [max value] [unit]
- Current Difference: [difference from ideal range]
"""
        
        if args.age and args.gender:
            prompt += """
#### 🔥 Metabolic Rate Analysis
- Basal Metabolic Rate (BMR): [value] kcal/day
- Description: This is the calories needed to maintain basic physiological functions at complete rest
"""
            if args.activity_level:
                prompt += """- Total Daily Energy Expenditure (TDEE): [value] kcal/day
- Activity Level: [description]
- Recommendation: [diet and exercise recommendations based on TDEE]
"""
        
        prompt += """
#### 💡 Health Recommendations
[Provide 3-5 personalized health recommendations based on the calculated results]

Please ensure all calculations are done using calculator-mcp tools to guarantee accuracy."""
        
        return prompt