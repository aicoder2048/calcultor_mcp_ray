# Calculator MCP Server Implementation Plan V1.5 - 模块化设计与配置修复

## 更新说明 (V1.0 → V1.5)

### 主要修复
1. **MCP配置路径修复**: 原配置使用环境变量`${PROJECT_DIR}`但该变量未正确设置导致Claude Code加载失败，修复方式是使用绝对路径替代环境变量
2. **工具参数类型修复**: 解决FastMCP工具注册时的参数类型识别问题，采用动态函数生成方案
3. **项目结构优化**: 基于实际实现调整文件结构和配置
4. **服务器入口修复**: 修正main函数和模块入口点

## Problem Statement and Objectives

### Problem Statement
需要创建一个功能完整的计算器MCP服务器，能够通过Model Context Protocol (MCP)协议在Claude Code中提供数学计算功能。该服务器应支持基础算术运算（加、减、乘、除）以及高级数学运算（平方、平方根、n次方根、立方）。**关键要求：采用模块化架构，每个Python文件独立实现一个功能，文件大小控制在200行以内，具备良好的可扩展性。**

### Objectives
1. **模块化架构**：每个数学运算独立实现为单独的模块，便于维护和扩展
2. **可扩展设计**：框架设计支持轻松添加新的数学运算功能
3. **文件大小控制**：每个Python文件不超过200行，保持代码简洁易读
4. **独立功能**：每个文件实现单一职责，降低耦合度
5. **统一接口**：所有运算模块遵循相同的接口设计
6. **项目级集成**：通过`.mcp.json`配置文件实现项目级MCP服务器配置，便于团队协作和版本控制
7. **便捷使用**：Claude Code自动检测并加载项目配置的MCP服务器

## Technical Approach and Architecture

### Technology Stack
- **语言**: Python 3.12+
- **框架**: FastMCP 2.0
- **验证**: Pydantic 2.10.6
- **测试**: pytest 8.3.4
- **包管理**: uv
- **数学库**: Python内置math模块

### Modular Architecture Design
```
calculator-mcp/
├── src/
│   └── calculator_mcp/
│       ├── __init__.py                 # 包初始化 (<50行)
│       ├── server.py                   # 主服务器入口 (<100行)
│       ├── base/
│       │   ├── __init__.py             # 基础模块 (<20行)
│       │   ├── operation.py            # 操作基类 (<100行)
│       │   ├── models.py              # 数据模型 (<50行)
│       │   └── registry.py            # 工具注册器 (<100行)
│       ├── operations/
│       │   ├── __init__.py             # 操作模块 (<50行)
│       │   ├── addition.py             # 加法运算 (<100行)
│       │   ├── subtraction.py          # 减法运算 (<100行)
│       │   ├── multiplication.py       # 乘法运算 (<100行)
│       │   ├── division.py             # 除法运算 (<150行)
│       │   ├── square.py              # 平方运算 (<100行)
│       │   ├── square_root.py         # 平方根运算 (<150行)
│       │   ├── nth_root.py            # n次方根运算 (<150行)
│       │   └── cube.py                # 立方运算 (<100行)
│       └── utils/
│           ├── __init__.py             # 工具模块 (<20行)
│           ├── validators.py           # 输入验证 (<100行)
│           ├── formatters.py          # 结果格式化 (<100行)
│           └── errors.py              # 错误处理 (<50行)
├── tests/
│   ├── test_operations/
│   │   ├── test_addition.py           # 加法测试 (<100行)
│   │   ├── test_division.py           # 除法测试 (<150行)
│   │   └── test_square_root.py        # 平方根测试 (<150行)
│   └── test_integration.py            # 集成测试 (<150行)
├── .mcp.json                           # Claude Code项目级MCP配置
├── main.py                            # 项目入口点
├── pyproject.toml                     # uv项目配置
├── fastmcp.json                       # FastMCP元数据
└── README.md
```

### Key Architecture Principles
1. **单一职责原则**：每个文件只负责一个具体的数学运算
2. **开放封闭原则**：对扩展开放，对修改封闭
3. **依赖倒置原则**：依赖抽象而非具体实现
4. **接口隔离原则**：细粒度的接口设计
5. **可组合性**：通过注册机制动态组合功能

## Step-by-Step Implementation Guide

### Phase 1: 基础框架搭建

#### 1.1 项目初始化
```bash
mkdir calculator-mcp
cd calculator-mcp
uv init --python 3.12
uv add fastmcp pydantic
uv add --dev pytest pytest-asyncio
```

#### 1.2 基础抽象类设计
```python
# src/calculator_mcp/base/operation.py
from abc import ABC, abstractmethod
from typing import Any, Type
from pydantic import BaseModel
from .models import OperationResult

class BaseOperation(ABC):
    """所有数学运算的基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """运算名称"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """运算描述"""
        pass
    
    @property
    @abstractmethod
    def input_model(self) -> Type[BaseModel]:
        """输入数据模型"""
        pass
    
    @abstractmethod
    async def execute(self, input_data: BaseModel) -> OperationResult:
        """执行运算"""
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        """验证输入数据"""
        pass
```

#### 1.3 数据模型定义（V1.5版本）
```python
# src/calculator_mcp/base/models.py
from pydantic import BaseModel, Field
from typing import Optional

class BinaryOperationInput(BaseModel):
    """二元运算输入模型"""
    a: float = Field(..., description="第一个操作数")
    b: float = Field(..., description="第二个操作数")

class UnaryOperationInput(BaseModel):
    """一元运算输入模型"""  
    value: float = Field(..., description="输入值")

class NthRootInput(BaseModel):
    """N次方根运算输入模型"""
    value: float = Field(..., description="被开方数")
    n: float = Field(2, description="根的次数，默认为2（平方根）")

class OperationResult(BaseModel):
    """运算结果模型"""
    success: bool = Field(..., description="运算是否成功")
    result: Optional[float] = Field(None, description="运算结果")
    error_message: Optional[str] = Field(None, description="错误信息")
    operation_name: str = Field(..., description="运算名称")

class CalculatorError(Exception):
    """计算器专用异常"""
    def __init__(self, message: str, operation: str = "unknown"):
        self.message = message
        self.operation = operation
        super().__init__(self.message)
```

#### 1.4 工具注册器（V1.5修复版 - 解决参数类型问题）
```python
# src/calculator_mcp/base/registry.py
from typing import Dict, Type
from .operation import BaseOperation
from .models import OperationResult
from fastmcp import FastMCP

class OperationRegistry:
    """运算工具注册器"""
    
    def __init__(self, mcp_server: FastMCP):
        self.mcp_server = mcp_server
        self.operations: Dict[str, BaseOperation] = {}
    
    def register(self, operation_class: Type[BaseOperation]) -> None:
        """注册一个运算操作"""
        operation = operation_class()
        self.operations[operation.name] = operation
        
        # 获取输入模型的字段信息
        input_model = operation.input_model
        
        # 使用动态函数创建解决参数类型识别问题
        def create_tool_function():
            """动态创建工具函数，确保FastMCP能正确识别参数类型"""
            fields = input_model.model_fields
            field_names = list(fields.keys())
            
            # 创建参数列表
            params = []
            for field_name, field_info in fields.items():
                field_type = field_info.annotation
                if hasattr(field_type, '__name__'):
                    type_name = field_type.__name__
                else:
                    type_name = str(field_type)
                params.append(f"{field_name}: {type_name}")
            
            params_str = ', '.join(params)
            kwargs_str = ', '.join(f"'{name}': {name}" for name in field_names)
            
            # 动态创建函数代码
            func_code = f"""
async def operation_tool({params_str}):
    try:
        kwargs = {{{kwargs_str}}}
        input_data = input_model(**kwargs)
        return await operation.execute(input_data)
    except Exception as e:
        return OperationResult(
            success=False,
            error_message=str(e),
            operation_name=operation.name
        )
"""
            
            # 执行代码创建函数
            local_vars = {
                'input_model': input_model,
                'operation': operation,
                'OperationResult': OperationResult
            }
            global_vars = {
                'input_model': input_model,
                'operation': operation,
                'OperationResult': OperationResult
            }
            exec(func_code, global_vars, local_vars)
            operation_tool = local_vars['operation_tool']
            operation_tool.__name__ = operation.name
            return operation_tool
        
        tool_function = create_tool_function()
        
        # 注册为MCP工具
        self.mcp_server.tool(description=operation.description)(tool_function)
    
    def get_operation(self, name: str) -> BaseOperation:
        """获取指定的运算操作"""
        return self.operations.get(name)
    
    def list_operations(self) -> list[str]:
        """列出所有已注册的运算"""
        return list(self.operations.keys())
```

### Phase 2: 基础运算实现

#### 2.1 加法运算模块
```python
# src/calculator_mcp/operations/addition.py
from typing import Type
from pydantic import BaseModel
from ..base.operation import BaseOperation
from ..base.models import BinaryOperationInput, OperationResult
from ..utils.validators import validate_finite_number
from ..utils.formatters import format_result

class AdditionOperation(BaseOperation):
    """加法运算实现"""
    
    @property
    def name(self) -> str:
        return "add"
    
    @property
    def description(self) -> str:
        return "执行加法运算：返回两个数的和 (a + b)"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return BinaryOperationInput
    
    def validate_input(self, input_data: BinaryOperationInput) -> bool:
        """验证输入数据"""
        return (validate_finite_number(input_data.a) and 
                validate_finite_number(input_data.b))
    
    async def execute(self, input_data: BinaryOperationInput) -> OperationResult:
        """执行加法运算"""
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                error_message="输入包含无效数值（无穷大或NaN）",
                operation_name=self.name
            )
        
        try:
            result = input_data.a + input_data.b
            formatted_result = format_result(result)
            
            return OperationResult(
                success=True,
                result=formatted_result,
                operation_name=self.name
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error_message=f"加法运算失败: {str(e)}",
                operation_name=self.name
            )
```

### Phase 3: 工具模块实现

#### 3.1 输入验证模块
```python
# src/calculator_mcp/utils/validators.py
import math
from typing import Union

def validate_finite_number(value: Union[int, float]) -> bool:
    """验证数值是否为有限数"""
    return not (math.isinf(value) or math.isnan(value))

def validate_non_zero(value: Union[int, float]) -> bool:
    """验证数值是否非零"""
    return value != 0

def validate_non_negative(value: Union[int, float]) -> bool:
    """验证数值是否非负"""
    return value >= 0

def validate_positive(value: Union[int, float]) -> bool:
    """验证数值是否为正数"""
    return value > 0
```

#### 3.2 结果格式化模块
```python
# src/calculator_mcp/utils/formatters.py
import math
from typing import Union

def format_result(value: Union[int, float], precision: int = 10) -> float:
    """格式化计算结果，处理浮点数精度问题"""
    if isinstance(value, int):
        return float(value)
    
    # 处理特殊值
    if math.isinf(value) or math.isnan(value):
        return value
    
    # 四舍五入到指定精度
    rounded = round(value, precision)
    
    # 如果结果非常接近整数，则返回整数形式
    if abs(rounded - round(rounded)) < 1e-10:
        return float(int(rounded))
    
    return rounded
```

### Phase 4: 主服务器组装（V1.5版本）

#### 4.1 服务器主入口
```python
# src/calculator_mcp/server.py
"""
计算器MCP服务器主入口
组装所有运算模块并启动服务器
"""
from fastmcp import FastMCP
from .base.registry import OperationRegistry
from .operations import (
    AdditionOperation,
    SubtractionOperation,
    MultiplicationOperation,
    DivisionOperation,
    SquareOperation,
    SquareRootOperation,
    NthRootOperation,
    CubeOperation,
)

def create_calculator_server() -> FastMCP:
    """创建计算器MCP服务器"""
    # 初始化FastMCP服务器
    mcp = FastMCP(
        name="calculator-mcp",
        version="1.0.0",
        instructions="Modular calculator MCP server with comprehensive math operations"
    )
    
    # 创建运算注册器
    registry = OperationRegistry(mcp)
    
    # 注册所有运算操作
    operations = [
        AdditionOperation,
        SubtractionOperation,
        MultiplicationOperation,
        DivisionOperation,
        SquareOperation,
        SquareRootOperation,
        NthRootOperation,
        CubeOperation,
    ]
    
    for operation_class in operations:
        registry.register(operation_class)
    
    return mcp

def main():
    """主函数"""
    server = create_calculator_server()
    server.run()

if __name__ == "__main__":
    main()
```

### Phase 5: Claude Code集成配置（V1.5修复版）

#### 5.1 项目级MCP配置文件（修复版 - 使用绝对路径）
```json
// .mcp.json (项目根目录)
{
  "mcpServers": {
    "calculator-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "calculator_mcp.server"],
      "env": {
        "PYTHONPATH": "/Users/szou/Python/Playground/Raymond/calculator-mcp/src"
      },
      "cwd": "/Users/szou/Python/Playground/Raymond/calculator-mcp"
    }
  }
}
```

**配置修复说明：**
- **问题**: 原配置使用`${PROJECT_DIR}`环境变量，但该变量在Claude Code环境中未正确设置
- **修复**: 使用绝对路径`/Users/szou/Python/Playground/Raymond/calculator-mcp`替代环境变量
- **PYTHONPATH**: 设置为绝对路径确保Python模块能正确导入
- **cwd**: 设置工作目录为项目根目录

#### 5.2 环境变量替代方案（可选）
```json
// .mcp.json (如果需要跨机器兼容性)
{
  "mcpServers": {
    "calculator-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "calculator_mcp.server"],
      "env": {
        "PYTHONPATH": "src"
      },
      "cwd": "/Users/szou/Python/Playground/Raymond/calculator-mcp"
    }
  }
}
```

#### 5.3 项目配置文件
```toml
# pyproject.toml
[project]
name = "calculator-mcp"
version = "1.0.0"
description = "A modular calculator MCP server for Claude Code"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastmcp>=2.0.0",
    "pydantic>=2.10.6",
]

[project.scripts]
calculator-mcp = "calculator_mcp.server:main"

[tool.uv]
dev-dependencies = [
    "pytest>=8.3.4",
    "pytest-asyncio>=0.21.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Phase 6: 测试和部署

#### 6.1 配置验证
```bash
# 验证uv环境
cd /Users/szou/Python/Playground/Raymond/calculator-mcp
uv sync

# 测试服务器启动
uv run python -m calculator_mcp.server

# 验证Claude Code配置
# 1. 确保.mcp.json在项目根目录
# 2. Claude Code会自动检测并提示加载
```

#### 6.2 使用说明
```bash
# 在Claude Code中使用：
> 使用calculator计算 25的平方根
> 计算 10 + 5 * 3  
> 计算 8 的立方根
```

## V1.5版本修复说明

### 1. MCP配置路径修复
**问题描述：**
- V1.0配置使用`${PROJECT_DIR}`环境变量
- Claude Code环境中该变量未正确设置
- 导致MCP服务器加载失败

**修复方案：**
- 使用绝对路径替代环境变量
- 设置正确的`PYTHONPATH`和`cwd`
- 确保Claude Code能正确定位和启动服务器

### 2. 工具参数类型修复
**问题描述：**
- FastMCP无法正确识别Pydantic模型的参数类型
- 工具注册时参数类型信息丢失

**修复方案：**
- 采用动态函数生成方式
- 通过exec动态创建具有明确参数类型的工具函数
- 确保FastMCP能正确解析参数类型和文档

### 3. 项目结构优化
- 基于实际实现调整模块结构
- 精简文件大小，确保符合200行限制
- 优化导入结构，避免循环依赖

### 4. 配置一致性
- 确保各配置文件间的版本和依赖一致
- 简化配置复杂度，提高可维护性

## Success Criteria

### Functional Requirements
- ✅ 实现8个独立的运算模块
- ✅ 每个Python文件控制在200行以内
- ✅ 模块化架构具备良好扩展性
- ✅ 统一的接口设计和错误处理
- ✅ MCP配置能在Claude Code中正确加载

### Quality Requirements
- ✅ 每个模块独立可测试
- ✅ 代码遵循单一职责原则
- ✅ 清晰的模块边界和依赖关系
- ✅ 工具参数类型正确识别和文档化

### Configuration Requirements
- ✅ 项目级MCP配置文件正确工作
- ✅ 绝对路径配置解决环境变量问题
- ✅ Claude Code无缝加载和使用
- ✅ 跨环境配置兼容性

## Conclusion

V1.5版本成功修复了V1.0中的关键配置和类型问题：

### 主要成就
1. **配置修复**: 解决了环境变量设置问题，使用绝对路径确保稳定性
2. **类型系统**: 修复了工具参数类型识别，提供完整的类型文档
3. **实用性**: 确保配置在实际Claude Code环境中正常工作
4. **架构稳定**: 保持模块化设计的同时提高了系统稳定性

该实现为生产环境提供了：
- **可靠的配置**: 绝对路径配置避免环境变量依赖
- **完整的类型信息**: 动态函数生成确保参数类型正确识别
- **良好的可扩展性**: 模块化架构支持轻松添加新功能
- **工程实践**: 遵循Python和FastMCP最佳实践

V1.5版本为构建生产就绪的计算器MCP服务器提供了坚实的基础。