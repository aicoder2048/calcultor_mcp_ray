# 营养配餐计算器 Prompt 实施计划

## 问题描述与目标

### 问题描述
用户需要一个智能的营养配餐工具，能够：
1. 根据个人健康数据计算营养需求
2. 分析食物营养成分和热量
3. 提供科学的膳食搭配建议
4. 制定个性化的饮食计划
5. 支持特殊饮食目标（减肥、增重、增肌等）
6. 考虑特殊人群的营养需求

### 目标
1. 创建一个交互式的营养配餐计算器Prompt
2. 提供科学准确的营养分析和建议
3. 支持多种饮食目标和特殊需求
4. 输出清晰的配餐方案和营养指导

## 技术方案

### 功能设计

#### 输入参数
- **height**: 身高（厘米）
- **weight**: 体重（公斤）
- **age**: 年龄
- **gender**: 性别（male/female）
- **activity_level**: 活动水平（与BMI计算器保持一致）
- **goal**: 饮食目标（maintain/lose_weight/gain_weight/gain_muscle）
- **dietary_restrictions**: 饮食限制（可选：vegetarian/vegan/gluten_free/dairy_free等）
- **target_weight**: 目标体重（可选，用于减重/增重计划）
- **timeline_weeks**: 时间目标（可选，多少周内达到目标）
- **language**: 输出语言（zh/en）

#### 计算功能
1. **基础营养需求计算**: 基于BMR和TDEE
2. **三大营养素分配**: 蛋白质、碳水化合物、脂肪比例
3. **维生素矿物质需求**: 基于年龄性别的RDA建议
4. **热量调整**: 根据饮食目标调整热量摄入
5. **餐次分配**: 早中晚餐及加餐的热量分配
6. **食物建议**: 推荐食物类别和份量

#### 输出内容
- 每日总热量需求
- 三大营养素分配（克数和百分比）
- 每餐热量和营养素分配
- 食物类别推荐和份量指导
- 饮食计划表格
- 个性化营养建议

### 实现步骤

1. **创建营养配餐Prompt类** (`nutrition_planner.py`)
   - 定义参数模型
   - 实现营养计算逻辑
   - 生成配餐建议

2. **集成到服务器**
   - 在`__init__.py`中导出
   - 在`server.py`中注册

3. **编写测试用例**
   - 测试不同饮食目标
   - 验证营养计算准确性
   - 测试特殊饮食限制

## 营养学参考标准

### 三大营养素推荐比例
- **一般成年人**: 蛋白质15-20%，碳水化合物50-65%，脂肪20-35%
- **减重期**: 蛋白质20-25%，碳水化合物40-50%，脂肪25-35%
- **增肌期**: 蛋白质25-30%，碳水化合物45-55%，脂肪20-30%

### 蛋白质需求
- **普通成年人**: 0.8g/kg体重
- **轻度运动**: 1.0-1.2g/kg体重
- **中度运动**: 1.2-1.6g/kg体重
- **高强度运动/增肌**: 1.6-2.2g/kg体重

### 热量调整策略
- **减重**: TDEE - 300-500千卡（每周减重0.3-0.5kg）
- **增重**: TDEE + 300-500千卡（每周增重0.3-0.5kg）
- **维持**: TDEE ± 100千卡

## 代码实现示例

### 参数模型
```python
class NutritionPlannerArguments(BaseModel):
    height: float = Field(..., description="身高（厘米）", gt=100, le=250)
    weight: float = Field(..., description="体重（公斤）", gt=30, le=200)
    age: int = Field(..., description="年龄", ge=1, le=120)
    gender: str = Field(..., description="性别: male/female")
    activity_level: str = Field("moderately_active", description="活动水平")
    goal: str = Field("maintain", description="饮食目标")
    dietary_restrictions: Optional[List[str]] = Field(None, description="饮食限制")
    target_weight: Optional[float] = Field(None, description="目标体重")
    timeline_weeks: Optional[int] = Field(None, description="时间目标（周）")
    language: str = Field("zh", description="输出语言")
```

### 营养计算逻辑
```python
def calculate_nutrition_needs(self, args: NutritionPlannerArguments) -> dict:
    # 计算BMR和TDEE
    bmr = self.calculate_bmr(args.weight, args.height, args.age, args.gender)
    tdee = self.calculate_tdee(bmr, args.activity_level)
    
    # 根据目标调整热量
    daily_calories = self.adjust_calories_for_goal(tdee, args.goal, args.target_weight)
    
    # 计算三大营养素
    macros = self.calculate_macronutrients(daily_calories, args.goal, args.weight)
    
    return {
        "daily_calories": daily_calories,
        "protein_grams": macros["protein"],
        "carbs_grams": macros["carbs"], 
        "fat_grams": macros["fat"]
    }
```

## 测试策略

### 单元测试
- 测试营养需求计算准确性
- 测试不同目标的热量调整
- 测试特殊饮食限制处理

### 集成测试
- 测试完整的配餐方案生成
- 测试不同参数组合
- 验证输出格式完整性

## 成功标准
1. ✅ 营养计算科学准确
2. ✅ 支持多种饮食目标
3. ✅ 提供个性化配餐建议
4. ✅ 生成清晰的营养指导
5. ✅ 所有测试用例通过

## 潜在挑战与解决方案

### 挑战1：营养学知识的准确性
**解决方案**: 基于权威营养学标准（WHO、中国营养学会等）

### 挑战2：食物数据库的复杂性
**解决方案**: 提供食物类别和营养密度建议，而非具体食物数据库

### 挑战3：个性化程度的平衡
**解决方案**: 提供通用科学建议，同时标注个体差异和专业咨询建议