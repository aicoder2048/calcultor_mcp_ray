"""
运算工具注册器
负责将运算操作注册为MCP工具
"""
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
        
        # 使用 exec 动态创建具有明确参数的工具函数
        def create_tool_function():
            # 获取模型字段信息
            fields = input_model.model_fields
            field_names = list(fields.keys())
            
            # 创建参数列表
            params = []
            for field_name, field_info in fields.items():
                # 获取类型注解
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