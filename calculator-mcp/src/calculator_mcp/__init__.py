"""
Calculator MCP Server
模块化的计算器MCP服务器
"""
from .server import create_calculator_server, main

__version__ = "1.0.0"
__all__ = ["create_calculator_server", "main"]