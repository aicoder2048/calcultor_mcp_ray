"""
计算器MCP服务器主入口
组装所有运算模块并启动服务器
"""
import asyncio
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