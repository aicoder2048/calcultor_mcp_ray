"""
计算器MCP服务器主入口
组装所有运算模块并启动服务器
"""
import asyncio
from fastmcp import FastMCP
from .base.registry import OperationRegistry
from .base.prompt_registry import PromptRegistry
from .operations import (
    AdditionOperation,
    SubtractionOperation,
    MultiplicationOperation,
    DivisionOperation,
    SquareOperation,
    SquareRootOperation,
    NthRootOperation,
    CubeOperation,
    AverageOperation,
)
from .prompts import (
    MultiplicationTablePrompt,
    HealthMetricsPrompt,
    NutritionPlannerPrompt,
)


def create_calculator_server() -> FastMCP:
    """创建计算器MCP服务器"""
    # 初始化FastMCP服务器
    mcp = FastMCP(
        name="calculator-mcp",
        version="2.0.0",
        instructions="Modular calculator MCP server with comprehensive math operations and interactive prompts"
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
        AverageOperation,
    ]
    
    for operation_class in operations:
        registry.register(operation_class)
    
    # 创建Prompt注册器
    prompt_registry = PromptRegistry(mcp)
    
    # 注册所有Prompt操作
    prompts = [
        MultiplicationTablePrompt,
        HealthMetricsPrompt,
        NutritionPlannerPrompt,
    ]
    
    for prompt_class in prompts:
        prompt_registry.register(prompt_class)
    
    return mcp


def main():
    """主函数"""
    server = create_calculator_server()
    server.run()


if __name__ == "__main__":
    main()