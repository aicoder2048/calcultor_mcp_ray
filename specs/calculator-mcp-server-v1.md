# Calculator MCP Server Implementation Plan V1 - Modular Design

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
│       │   ├── models.py              # 数据模型 (<150行)
│       │   └── registry.py            # 工具注册器 (<100行)
│       ├── operations/
│       │   ├── __init__.py             # 操作模块 (<50行)
│       │   ├── addition.py             # 加法运算 (<150行)
│       │   ├── subtraction.py          # 减法运算 (<150行)
│       │   ├── multiplication.py       # 乘法运算 (<150行)
│       │   ├── division.py             # 除法运算 (<200行)
│       │   ├── square.py              # 平方运算 (<150行)
│       │   ├── square_root.py         # 平方根运算 (<200行)
│       │   ├── nth_root.py            # n次方根运算 (<200行)
│       │   └── cube.py                # 立方运算 (<150行)
│       └── utils/
│           ├── __init__.py             # 工具模块 (<20行)
│           ├── validators.py           # 输入验证 (<150行)
│           ├── formatters.py          # 结果格式化 (<100行)
│           └── errors.py              # 错误处理 (<100行)
├── tests/
│   ├── test_operations/
│   │   ├── test_addition.py           # 加法测试 (<100行)
│   │   ├── test_subtraction.py        # 减法测试 (<100行)
│   │   ├── test_multiplication.py     # 乘法测试 (<100行)
│   │   ├── test_division.py           # 除法测试 (<150行)
│   │   ├── test_square.py             # 平方测试 (<100行)
│   │   ├── test_square_root.py        # 平方根测试 (<150行)
│   │   ├── test_nth_root.py           # n次方根测试 (<150行)
│   │   └── test_cube.py               # 立方测试 (<100行)
│   ├── test_base/
│   │   ├── test_registry.py           # 注册器测试 (<100行)
│   │   └── test_models.py             # 模型测试 (<100行)
│   └── test_integration.py            # 集成测试 (<150行)
├── .mcp.json                           # Claude Code项目级MCP配置
├── pyproject.toml
├── fastmcp.json
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
from typing import Any, Dict, Type
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

#### 1.3 数据模型定义
```python
# src/calculator_mcp/base/models.py
from pydantic import BaseModel, Field
from typing import Optional, Union
from decimal import Decimal

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

#### 1.4 工具注册器
```python
# src/calculator_mcp/base/registry.py
from typing import Dict, Type
from .operation import BaseOperation
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
        
        # 动态注册为MCP工具
        @self.mcp_server.tool(description=operation.description)
        async def operation_tool(input_data: operation.input_model):
            try:
                return await operation.execute(input_data)
            except Exception as e:
                return OperationResult(
                    success=False,
                    error_message=str(e),
                    operation_name=operation.name
                )
        
        # 设置工具名称
        operation_tool.__name__ = operation.name
    
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

#### 2.2 除法运算模块（错误处理示例）
```python
# src/calculator_mcp/operations/division.py
from typing import Type
from pydantic import BaseModel
from ..base.operation import BaseOperation
from ..base.models import BinaryOperationInput, OperationResult, CalculatorError
from ..utils.validators import validate_finite_number, validate_non_zero
from ..utils.formatters import format_result

class DivisionOperation(BaseOperation):
    """除法运算实现"""
    
    @property
    def name(self) -> str:
        return "divide"
    
    @property
    def description(self) -> str:
        return "执行除法运算：返回两个数的商 (a ÷ b)"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return BinaryOperationInput
    
    def validate_input(self, input_data: BinaryOperationInput) -> bool:
        """验证输入数据"""
        return (validate_finite_number(input_data.a) and 
                validate_finite_number(input_data.b) and
                validate_non_zero(input_data.b))
    
    async def execute(self, input_data: BinaryOperationInput) -> OperationResult:
        """执行除法运算"""
        # 检查除零错误
        if input_data.b == 0:
            return OperationResult(
                success=False,
                error_message="错误：除数不能为零",
                operation_name=self.name
            )
        
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                error_message="输入包含无效数值",
                operation_name=self.name
            )
        
        try:
            result = input_data.a / input_data.b
            formatted_result = format_result(result)
            
            return OperationResult(
                success=True,
                result=formatted_result,
                operation_name=self.name
            )
        except ZeroDivisionError:
            return OperationResult(
                success=False,
                error_message="错误：除数不能为零",
                operation_name=self.name
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error_message=f"除法运算失败: {str(e)}",
                operation_name=self.name
            )
```

### Phase 3: 高级运算实现

#### 3.1 平方根运算模块
```python
# src/calculator_mcp/operations/square_root.py
import math
from typing import Type
from pydantic import BaseModel
from ..base.operation import BaseOperation
from ..base.models import UnaryOperationInput, OperationResult
from ..utils.validators import validate_finite_number, validate_non_negative
from ..utils.formatters import format_result

class SquareRootOperation(BaseOperation):
    """平方根运算实现"""
    
    @property
    def name(self) -> str:
        return "square_root"
    
    @property
    def description(self) -> str:
        return "计算平方根：返回输入值的平方根 (√value)"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return UnaryOperationInput
    
    def validate_input(self, input_data: UnaryOperationInput) -> bool:
        """验证输入数据"""
        return (validate_finite_number(input_data.value) and 
                validate_non_negative(input_data.value))
    
    async def execute(self, input_data: UnaryOperationInput) -> OperationResult:
        """执行平方根运算"""
        if input_data.value < 0:
            return OperationResult(
                success=False,
                error_message="错误：不能计算负数的平方根",
                operation_name=self.name
            )
        
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                error_message="输入包含无效数值",
                operation_name=self.name
            )
        
        try:
            result = math.sqrt(input_data.value)
            formatted_result = format_result(result)
            
            return OperationResult(
                success=True,
                result=formatted_result,
                operation_name=self.name
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error_message=f"平方根运算失败: {str(e)}",
                operation_name=self.name
            )
```

#### 3.2 N次方根运算模块
```python
# src/calculator_mcp/operations/nth_root.py
import math
from typing import Type
from pydantic import BaseModel
from ..base.operation import BaseOperation
from ..base.models import NthRootInput, OperationResult
from ..utils.validators import validate_finite_number, validate_non_zero
from ..utils.formatters import format_result

class NthRootOperation(BaseOperation):
    """N次方根运算实现"""
    
    @property
    def name(self) -> str:
        return "nth_root"
    
    @property
    def description(self) -> str:
        return "计算N次方根：返回输入值的N次方根 (value^(1/n))"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return NthRootInput
    
    def validate_input(self, input_data: NthRootInput) -> bool:
        """验证输入数据"""
        return (validate_finite_number(input_data.value) and 
                validate_finite_number(input_data.n) and
                validate_non_zero(input_data.n))
    
    async def execute(self, input_data: NthRootInput) -> OperationResult:
        """执行N次方根运算"""
        if input_data.n == 0:
            return OperationResult(
                success=False,
                error_message="错误：根的次数不能为零",
                operation_name=self.name
            )
        
        # 处理负数的偶数次根
        if input_data.value < 0 and input_data.n % 2 == 0:
            return OperationResult(
                success=False,
                error_message="错误：不能计算负数的偶数次根",
                operation_name=self.name
            )
        
        if not self.validate_input(input_data):
            return OperationResult(
                success=False,
                error_message="输入包含无效数值",
                operation_name=self.name
            )
        
        try:
            # 处理负数的奇数次根
            if input_data.value < 0 and input_data.n % 2 == 1:
                result = -(-input_data.value) ** (1/input_data.n)
            else:
                result = input_data.value ** (1/input_data.n)
            
            formatted_result = format_result(result)
            
            return OperationResult(
                success=True,
                result=formatted_result,
                operation_name=self.name
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error_message=f"N次方根运算失败: {str(e)}",
                operation_name=self.name
            )
```

### Phase 4: 工具模块实现

#### 4.1 输入验证模块
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

def validate_integer(value: Union[int, float]) -> bool:
    """验证数值是否为整数"""
    return value == int(value)

def validate_in_range(value: Union[int, float], min_val: float = None, max_val: float = None) -> bool:
    """验证数值是否在指定范围内"""
    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
    return True
```

#### 4.2 结果格式化模块
```python
# src/calculator_mcp/utils/formatters.py
import math
from typing import Union

def format_result(value: Union[int, float], precision: int = 10) -> float:
    """格式化计算结果，处理浮点数精度问题"""
    if isinstance(value, int):
        return float(value)
    
    # 处理特殊值
    if math.isinf(value):
        return value
    if math.isnan(value):
        return value
    
    # 四舍五入到指定精度
    rounded = round(value, precision)
    
    # 如果结果非常接近整数，则返回整数形式
    if abs(rounded - round(rounded)) < 1e-10:
        return float(int(rounded))
    
    return rounded

def format_error_message(operation: str, error: str) -> str:
    """格式化错误消息"""
    return f"[{operation}] {error}"

def is_close_to_integer(value: float, tolerance: float = 1e-10) -> bool:
    """检查浮点数是否接近整数"""
    return abs(value - round(value)) < tolerance
```

### Phase 5: 主服务器组装

#### 5.1 服务器主入口
```python
# src/calculator_mcp/server.py
import asyncio
from fastmcp import FastMCP
from .base.registry import OperationRegistry
from .operations.addition import AdditionOperation
from .operations.subtraction import SubtractionOperation
from .operations.multiplication import MultiplicationOperation
from .operations.division import DivisionOperation
from .operations.square import SquareOperation
from .operations.square_root import SquareRootOperation
from .operations.nth_root import NthRootOperation
from .operations.cube import CubeOperation

def create_calculator_server() -> FastMCP:
    """创建计算器MCP服务器"""
    # 初始化FastMCP服务器
    mcp = FastMCP(
        name="calculator-mcp",
        version="1.0.0",
        description="Modular calculator MCP server with comprehensive math operations"
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

async def main():
    """主函数"""
    server = create_calculator_server()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Phase 6: Claude Code集成配置

#### 6.1 项目级MCP配置文件
```json
// .mcp.json (项目根目录)
{
  "mcpServers": {
    "calculator-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--python",
        "3.12",
        "python",
        "${PROJECT_DIR}/src/calculator_mcp/server.py"
      ],
      "env": {
        "PYTHONPATH": "${PROJECT_DIR}/src"
      }
    }
  }
}
```

#### 6.2 环境变量配置
```json
// .mcp.json (支持环境变量扩展)
{
  "mcpServers": {
    "calculator-mcp": {
      "command": "${UV_PATH:-uv}",
      "args": [
        "run",
        "--python",
        "${PYTHON_VERSION:-3.12}",
        "python",
        "${PROJECT_DIR}/src/calculator_mcp/server.py"
      ],
      "env": {
        "PYTHONPATH": "${PROJECT_DIR}/src",
        "LOG_LEVEL": "${LOG_LEVEL:-INFO}"
      }
    }
  }
}
```

#### 6.3 开发环境配置
```json
// .mcp.json (开发模式)
{
  "mcpServers": {
    "calculator-mcp-dev": {
      "command": "uv",
      "args": [
        "run",
        "--reload",  // 支持热重载
        "python",
        "-m",
        "calculator_mcp.server"
      ],
      "env": {
        "PYTHONPATH": "${PROJECT_DIR}/src",
        "DEBUG": "true"
      }
    }
  }
}
```

#### 6.4 使用说明
```bash
# 1. 在项目根目录创建.mcp.json配置文件
# 2. Claude Code会自动检测并提示是否使用项目配置的MCP服务器
# 3. 接受后即可在Claude Code中使用计算器功能

# 验证配置：
claude mcp list  # 查看已加载的MCP服务器

# 在Claude Code中使用：
> 使用calculator计算 25的平方根
> 计算 10 + 5 * 3
```

### Phase 7: 部署和文档
```

## Testing Strategy

### 1. 单元测试（每个运算模块）
```python
# tests/test_operations/test_addition.py
import pytest
from calculator_mcp.operations.addition import AdditionOperation
from calculator_mcp.base.models import BinaryOperationInput

class TestAdditionOperation:
    def setup_method(self):
        self.operation = AdditionOperation()
    
    async def test_simple_addition(self):
        input_data = BinaryOperationInput(a=5, b=3)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == 8.0
    
    async def test_negative_numbers(self):
        input_data = BinaryOperationInput(a=-5, b=3)
        result = await self.operation.execute(input_data)
        assert result.success is True
        assert result.result == -2.0
    
    # 更多测试案例...
```

### 2. 集成测试
```python
# tests/test_integration.py
import pytest
from calculator_mcp.server import create_calculator_server

class TestServerIntegration:
    def setup_method(self):
        self.server = create_calculator_server()
    
    async def test_all_operations_registered(self):
        """测试所有运算都已正确注册"""
        # 验证工具数量
        # 验证工具名称
        # 验证工具可调用性
        pass
```

### 3. 模块化测试策略
- **隔离测试**: 每个模块独立测试，不依赖其他模块
- **接口测试**: 验证所有模块遵循相同接口规范
- **扩展测试**: 验证新增模块的注册和使用

## Success Criteria

### Functional Requirements
- ✅ 实现8个独立的运算模块
- ✅ 每个Python文件控制在200行以内
- ✅ 模块化架构具备良好扩展性
- ✅ 统一的接口设计和错误处理

### Quality Requirements
- ✅ 每个模块独立可测试，覆盖率>95%
- ✅ 代码遵循单一职责原则
- ✅ 清晰的模块边界和依赖关系
- ✅ 完整的文档和示例

### Extensibility Requirements
- ✅ 新增运算模块无需修改现有代码
- ✅ 支持运算模块的热插拔
- ✅ 清晰的扩展接口和文档

## Extension Examples

### 添加新运算模块示例
```python
# src/calculator_mcp/operations/power.py
from typing import Type
from pydantic import BaseModel
from ..base.operation import BaseOperation
from ..base.models import BinaryOperationInput, OperationResult
from ..utils.validators import validate_finite_number
from ..utils.formatters import format_result

class PowerOperation(BaseOperation):
    """幂运算实现 (a^b)"""
    
    @property
    def name(self) -> str:
        return "power"
    
    @property
    def description(self) -> str:
        return "计算幂运算：返回a的b次方 (a^b)"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return BinaryOperationInput
    
    def validate_input(self, input_data: BinaryOperationInput) -> bool:
        return (validate_finite_number(input_data.a) and 
                validate_finite_number(input_data.b))
    
    async def execute(self, input_data: BinaryOperationInput) -> OperationResult:
        # 实现幂运算逻辑
        try:
            result = input_data.a ** input_data.b
            return OperationResult(
                success=True,
                result=format_result(result),
                operation_name=self.name
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error_message=f"幂运算失败: {str(e)}",
                operation_name=self.name
            )
```

### 动态模块发现机制
```python
# src/calculator_mcp/utils/discovery.py
import importlib
import pkgutil
from typing import List, Type
from ..base.operation import BaseOperation

def discover_operations(package_name: str = "calculator_mcp.operations") -> List[Type[BaseOperation]]:
    """自动发现所有运算模块"""
    operations = []
    package = importlib.import_module(package_name)
    
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")
        
        # 查找继承自BaseOperation的类
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and 
                issubclass(attr, BaseOperation) and 
                attr != BaseOperation):
                operations.append(attr)
    
    return operations
```

## Conclusion

这个模块化设计的计算器MCP服务器实施计划完全满足了您的要求：

1. **严格的文件大小控制**: 每个Python文件都控制在200行以内
2. **完全模块化架构**: 每个数学运算独立实现为单独模块
3. **高度可扩展性**: 新增功能无需修改现有代码，只需添加新模块并注册
4. **单一职责原则**: 每个文件只负责一个具体功能
5. **统一接口设计**: 所有运算模块遵循相同的基类接口

该架构设计具备以下优势：
- **易于维护**: 模块间低耦合，修改某个运算不影响其他功能
- **便于测试**: 每个模块可独立测试，测试用例清晰
- **支持扩展**: 通过注册机制轻松添加新的数学运算
- **代码重用**: 公共逻辑提取到基类和工具模块
- **良好实践**: 遵循SOLID原则和Python最佳实践

这个设计为构建一个专业、可靠且易于扩展的计算器MCP服务器提供了坚实的架构基础。