# BMI与健康指标计算器 Prompt 实施计划

## 问题描述与目标

### 问题描述
用户需要一个综合的健康指标计算工具，能够：
1. 计算BMI（身体质量指数）
2. 评估BMI对应的健康状态
3. 计算理想体重范围
4. 提供基础代谢率(BMR)计算
5. 估算每日热量需求(TDEE)
6. 支持公制和英制单位

### 目标
1. 创建一个交互式的BMI健康指标计算器Prompt
2. 提供全面的健康指标分析
3. 支持多种计算公式和标准
4. 输出清晰的健康建议和参考值

## 技术方案

### 功能设计

#### 输入参数
- **height**: 身高（厘米或英寸）
- **weight**: 体重（公斤或磅）
- **age**: 年龄（可选，用于BMR计算）
- **gender**: 性别（可选，用于BMR计算）
- **activity_level**: 活动水平（可选，用于TDEE计算）
- **unit_system**: 单位制（metric/imperial）

#### 计算功能
1. **BMI计算**: weight(kg) / (height(m))²
2. **BMI分类**: 根据WHO标准分类
3. **理想体重**: 基于BMI 18.5-24.9范围
4. **BMR计算**: 使用Mifflin-St Jeor公式
5. **TDEE计算**: BMR × 活动系数

#### 输出内容
- BMI值和健康状态评估
- 理想体重范围
- BMR基础代谢率
- TDEE每日热量需求
- 个性化健康建议

### 实现步骤

1. **创建健康指标Prompt类** (`health_metrics.py`)
   - 定义参数模型
   - 实现计算逻辑
   - 生成格式化输出

2. **集成到服务器**
   - 在`__init__.py`中导出
   - 在`server.py`中注册

3. **编写测试用例**
   - 测试不同单位制
   - 验证计算准确性
   - 测试边界条件

## 代码实现示例

### 参数模型
```python
class HealthMetricsArguments(BaseModel):
    height: float = Field(..., description="身高", gt=0)
    weight: float = Field(..., description="体重", gt=0)
    age: Optional[int] = Field(None, description="年龄", ge=1, le=120)
    gender: Optional[str] = Field(None, description="性别: male/female")
    activity_level: Optional[str] = Field("sedentary", description="活动水平")
    unit_system: str = Field("metric", description="单位制: metric/imperial")
    language: str = Field("zh", description="输出语言: zh/en")
```

### BMI计算逻辑
```python
def calculate_bmi(weight: float, height: float, unit_system: str) -> float:
    if unit_system == "imperial":
        # 转换英制单位
        weight_kg = weight * 0.453592
        height_m = height * 0.0254
    else:
        height_m = height / 100
        weight_kg = weight
    
    return weight_kg / (height_m ** 2)
```

## 测试策略

### 单元测试
- 测试BMI计算准确性
- 测试单位转换
- 测试参数验证

### 集成测试
- 测试完整的Prompt生成流程
- 测试不同参数组合
- 验证输出格式

## 成功标准
1. ✅ BMI计算准确无误
2. ✅ 支持公制和英制单位
3. ✅ 提供完整的健康指标分析
4. ✅ 生成清晰的健康建议
5. ✅ 所有测试用例通过

## 潜在挑战与解决方案

### 挑战1：单位转换准确性
**解决方案**: 使用精确的转换系数，并在测试中验证

### 挑战2：健康建议的准确性
**解决方案**: 基于WHO和权威健康组织的标准

### 挑战3：活动水平的主观性
**解决方案**: 提供清晰的活动水平描述和示例