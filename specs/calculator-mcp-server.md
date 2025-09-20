# Calculator MCP Server Implementation Plan

## Problem Statement and Objectives

### Problem Statement
需要创建一个功能完整的计算器MCP服务器，能够通过Model Context Protocol (MCP)协议在Claude Code中提供数学计算功能。该服务器应支持基础算术运算（加、减、乘、除）以及高级数学运算（平方、平方根、n次方根、立方）。

### Objectives
1. **实现MCP服务器**：使用FastMCP框架构建符合MCP标准的计算器服务器
2. **提供数学工具**：实现8个核心数学运算功能作为MCP工具
3. **确保易用性**：在Claude Code中可直接安装和使用
4. **保证可靠性**：实现完善的错误处理和输入验证
5. **支持扩展**：架构设计应便于添加新的数学运算功能

## Technical Approach and Architecture

### Technology Stack
- **语言**: Python 3.12+
- **框架**: FastMCP 2.0
- **验证**: Pydantic 2.10.6
- **测试**: pytest 8.3.4
- **包管理**: uv
- **数学库**: Python内置math模块

### Architecture Design
```
┌─────────────────────┐
│   Claude Code       │
├─────────────────────┤
│   MCP Protocol      │
├─────────────────────┤
│  FastMCP Server     │
├─────────────────────┤
│   Tool Registry     │
├─────────────────────┤
│  Math Operations    │
│  ┌────────────────┐ │
│  │ Basic Ops      │ │
│  │ - Add          │ │
│  │ - Subtract     │ │
│  │ - Multiply     │ │
│  │ - Divide       │ │
│  ├────────────────┤ │
│  │ Advanced Ops   │ │
│  │ - Square       │ │
│  │ - Square Root  │ │
│  │ - Nth Root     │ │
│  │ - Cube         │ │
│  └────────────────┘ │
└─────────────────────┘
```

### Key Design Decisions
1. **单文件实现**：将所有功能集成在一个Python文件中，便于部署
2. **工具分离**：每个数学运算作为独立的MCP工具，提高可维护性
3. **类型安全**：使用Pydantic模型定义所有输入参数
4. **错误处理**：统一的错误处理机制，返回清晰的错误信息
5. **国际化支持**：支持中英文描述和错误提示

## Step-by-Step Implementation Guide

### Phase 1: Project Setup
1. **初始化项目结构**
   ```bash
   mkdir calculator-mcp
   cd calculator-mcp
   uv init
   ```

2. **安装依赖**
   ```bash
   uv add fastmcp pydantic
   uv add --dev pytest pytest-asyncio
   ```

3. **创建项目文件结构**
   ```
   calculator-mcp/
   ├── pyproject.toml
   ├── README.md
   ├── src/
   │   └── calculator_mcp/
   │       ├── __init__.py
   │       └── server.py
   ├── tests/
   │   └── test_calculator.py
   └── fastmcp.json
   ```

### Phase 2: Implement Core Calculator Server

#### 2.1 Basic Server Setup
```python
# src/calculator_mcp/server.py
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import math
from typing import Optional, Union

# 创建FastMCP服务器实例
mcp = FastMCP(
    name="calculator-mcp",
    version="1.0.0",
    description="A comprehensive calculator MCP server with basic and advanced math operations"
)
```

#### 2.2 Define Input Models
```python
# 基础二元运算输入模型
class BinaryOperationInput(BaseModel):
    a: float = Field(..., description="第一个操作数")
    b: float = Field(..., description="第二个操作数")

# 单元运算输入模型
class UnaryOperationInput(BaseModel):
    value: float = Field(..., description="输入值")

# N次方根输入模型
class NthRootInput(BaseModel):
    value: float = Field(..., description="被开方数")
    n: float = Field(2, description="根的次数，默认为2（平方根）")
```

#### 2.3 Implement Basic Arithmetic Operations
```python
@mcp.tool(
    description="执行加法运算：返回两个数的和"
)
def add(input: BinaryOperationInput) -> float:
    """计算 a + b"""
    return input.a + input.b

@mcp.tool(
    description="执行减法运算：返回两个数的差"
)
def subtract(input: BinaryOperationInput) -> float:
    """计算 a - b"""
    return input.a - input.b

@mcp.tool(
    description="执行乘法运算：返回两个数的积"
)
def multiply(input: BinaryOperationInput) -> float:
    """计算 a × b"""
    return input.a * input.b

@mcp.tool(
    description="执行除法运算：返回两个数的商"
)
def divide(input: BinaryOperationInput) -> float:
    """计算 a ÷ b，处理除零错误"""
    if input.b == 0:
        raise ValueError("错误：除数不能为零")
    return input.a / input.b
```

#### 2.4 Implement Advanced Math Operations
```python
@mcp.tool(
    description="计算平方：返回输入值的平方"
)
def square(input: UnaryOperationInput) -> float:
    """计算 value²"""
    return input.value ** 2

@mcp.tool(
    description="计算平方根：返回输入值的平方根"
)
def square_root(input: UnaryOperationInput) -> float:
    """计算 √value"""
    if input.value < 0:
        raise ValueError("错误：不能计算负数的平方根")
    return math.sqrt(input.value)

@mcp.tool(
    description="计算N次方根：返回输入值的N次方根"
)
def nth_root(input: NthRootInput) -> float:
    """计算 value^(1/n)"""
    if input.n == 0:
        raise ValueError("错误：根的次数不能为零")
    
    # 处理负数的奇数次根
    if input.value < 0 and input.n % 2 == 1:
        return -(-input.value) ** (1/input.n)
    elif input.value < 0:
        raise ValueError("错误：不能计算负数的偶数次根")
    
    return input.value ** (1/input.n)

@mcp.tool(
    description="计算立方：返回输入值的立方"
)
def cube(input: UnaryOperationInput) -> float:
    """计算 value³"""
    return input.value ** 3
```

#### 2.5 Add Main Entry Point
```python
if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run())
```

### Phase 3: Create Configuration Files

#### 3.1 FastMCP Configuration
```json
// fastmcp.json
{
  "name": "calculator-mcp",
  "version": "1.0.0",
  "description": "Calculator MCP Server with comprehensive math operations",
  "main": "src/calculator_mcp/server.py",
  "requirements": [
    "fastmcp>=2.0.0",
    "pydantic>=2.10.0"
  ],
  "python": ">=3.12"
}
```

#### 3.2 PyProject Configuration
```toml
# pyproject.toml
[project]
name = "calculator-mcp"
version = "1.0.0"
description = "A calculator MCP server for Claude Code"
requires-python = ">=3.12"
dependencies = [
    "fastmcp>=2.0.0",
    "pydantic>=2.10.6",
]

[project.scripts]
calculator-mcp = "calculator_mcp.server:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Phase 4: Implement Tests

```python
# tests/test_calculator.py
import pytest
from calculator_mcp.server import (
    add, subtract, multiply, divide,
    square, square_root, nth_root, cube,
    BinaryOperationInput, UnaryOperationInput, NthRootInput
)

class TestBasicOperations:
    def test_add(self):
        result = add(BinaryOperationInput(a=5, b=3))
        assert result == 8
    
    def test_subtract(self):
        result = subtract(BinaryOperationInput(a=10, b=3))
        assert result == 7
    
    def test_multiply(self):
        result = multiply(BinaryOperationInput(a=4, b=5))
        assert result == 20
    
    def test_divide(self):
        result = divide(BinaryOperationInput(a=15, b=3))
        assert result == 5
    
    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="除数不能为零"):
            divide(BinaryOperationInput(a=10, b=0))

class TestAdvancedOperations:
    def test_square(self):
        result = square(UnaryOperationInput(value=4))
        assert result == 16
    
    def test_square_root(self):
        result = square_root(UnaryOperationInput(value=16))
        assert result == 4
    
    def test_negative_square_root(self):
        with pytest.raises(ValueError, match="不能计算负数的平方根"):
            square_root(UnaryOperationInput(value=-4))
    
    def test_cube(self):
        result = cube(UnaryOperationInput(value=3))
        assert result == 27
    
    def test_nth_root(self):
        result = nth_root(NthRootInput(value=27, n=3))
        assert abs(result - 3) < 0.0001  # 浮点数精度比较
```

### Phase 5: Claude Code Integration

#### 5.1 Local Development Installation
```bash
# 在项目目录运行服务器进行测试
uv run python src/calculator_mcp/server.py

# 添加到Claude Code（开发模式）
claude mcp add calculator-dev -- uv run python /path/to/calculator-mcp/src/calculator_mcp/server.py
```

#### 5.2 Production Installation
```bash
# 方式1：使用pip包（需要先发布到PyPI）
claude mcp add calculator -- uv pip install calculator-mcp && calculator-mcp

# 方式2：使用GitHub直接安装
claude mcp add calculator -- uv pip install git+https://github.com/yourusername/calculator-mcp.git && calculator-mcp

# 方式3：使用npx（需要创建npm包装器）
claude mcp add calculator -- npx calculator-mcp-server
```

## Potential Challenges and Solutions

### Challenge 1: 浮点数精度问题
**问题**: 浮点数运算可能导致精度丢失
**解决方案**: 
- 使用Python的`decimal.Decimal`类处理高精度计算
- 在输出时合理控制小数位数
- 对于比较操作使用误差范围

### Challenge 2: 错误处理和用户体验
**问题**: 数学错误（如除零、负数平方根）需要友好提示
**解决方案**:
- 统一的错误处理装饰器
- 返回结构化的错误信息
- 支持中英文错误提示

### Challenge 3: 性能优化
**问题**: 复杂运算可能影响响应速度
**解决方案**:
- 使用缓存机制存储常用计算结果
- 对于大数运算设置合理的限制
- 实现异步处理机制

### Challenge 4: 扩展性设计
**问题**: 后续可能需要添加更多数学功能
**解决方案**:
- 模块化设计，每类运算独立模块
- 使用插件机制动态加载新功能
- 维护清晰的API版本管理

## Testing Strategy

### 1. Unit Testing
- **覆盖率目标**: 95%以上
- **测试内容**:
  - 所有数学运算的正常情况
  - 边界条件（零、负数、极大值、极小值）
  - 错误情况（除零、无效输入）
  - 输入验证（类型检查、范围验证）

### 2. Integration Testing
- **MCP协议兼容性测试**
  - 工具发现机制
  - 参数传递正确性
  - 响应格式规范性

- **Claude Code集成测试**
  - 安装流程验证
  - 工具调用测试
  - 错误处理测试

### 3. Performance Testing
- **响应时间**: 所有运算应在100ms内完成
- **并发处理**: 支持多个请求并发处理
- **内存使用**: 监控内存泄漏

### 4. User Acceptance Testing
- **场景测试**: 模拟实际使用场景
- **易用性测试**: 命令格式和参数是否直观
- **文档完整性**: 确保所有功能都有清晰文档

## Success Criteria

### Functional Requirements
- ✅ 实现所有8个数学运算功能
- ✅ 所有功能通过单元测试
- ✅ 错误处理机制完善
- ✅ 支持中文描述和提示

### Performance Requirements
- ✅ 响应时间 < 100ms
- ✅ 内存使用 < 50MB
- ✅ CPU使用率合理

### Integration Requirements
- ✅ 成功在Claude Code中安装
- ✅ 所有工具可被发现和调用
- ✅ 返回结果格式正确

### Quality Requirements
- ✅ 代码测试覆盖率 > 95%
- ✅ 无已知bug
- ✅ 文档完整清晰
- ✅ 遵循Python最佳实践

## Additional Enhancements

### Future Features
1. **科学计算功能**
   - 三角函数（sin, cos, tan）
   - 对数运算（log, ln）
   - 指数运算（exp）
   - 阶乘和组合数学

2. **高级功能**
   - 表达式解析和计算
   - 单位转换
   - 统计计算
   - 矩阵运算

3. **用户体验优化**
   - 计算历史记录
   - 批量计算支持
   - 自定义精度设置
   - 结果格式化选项

## Code Examples

### Example 1: Simple Usage in Claude Code
```python
# 在Claude Code中使用
> 使用calculator计算 25的平方根
# Claude将调用: calculator.square_root({"value": 25})
# 返回: 5.0

> 计算 (10 + 5) × 3
# Claude将调用:
# 1. calculator.add({"a": 10, "b": 5})  # = 15
# 2. calculator.multiply({"a": 15, "b": 3})  # = 45
# 返回: 45.0
```

### Example 2: Error Handling
```python
# 错误处理示例
> 使用calculator计算 10 除以 0
# Claude将调用: calculator.divide({"a": 10, "b": 0})
# 返回错误: "错误：除数不能为零"

> 计算 -16 的平方根
# Claude将调用: calculator.square_root({"value": -16})
# 返回错误: "错误：不能计算负数的平方根"
```

### Example 3: Advanced Calculations
```python
# 复杂计算示例
> 计算 8 的立方根
# Claude将调用: calculator.nth_root({"value": 8, "n": 3})
# 返回: 2.0

> 计算 2 的 10 次方
# Claude可以通过多次调用square实现或扩展power功能
```

## Deployment Guide

### Local Development
1. Clone repository
2. Install dependencies with `uv sync`
3. Run tests with `uv run pytest`
4. Start server with `uv run python src/calculator_mcp/server.py`

### Production Deployment
1. Package the application
2. Publish to PyPI or private registry
3. Create installation script
4. Document installation process
5. Provide troubleshooting guide

## Maintenance and Support

### Version Management
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Maintain backward compatibility
- Document all breaking changes

### Documentation
- API documentation with examples
- User guide for Claude Code integration
- Developer guide for contributions
- Troubleshooting FAQ

### Monitoring
- Error logging and reporting
- Usage statistics
- Performance metrics
- User feedback collection

## Conclusion

这个计算器MCP服务器实施计划提供了一个完整的路线图，从初始设计到最终部署。通过使用FastMCP框架和遵循最佳实践，我们可以创建一个可靠、高效且易于使用的计算器服务，完美集成到Claude Code中。

该计划强调了模块化设计、完善的错误处理和全面的测试策略，确保服务器不仅满足当前需求，还具备良好的扩展性以支持未来功能增强。