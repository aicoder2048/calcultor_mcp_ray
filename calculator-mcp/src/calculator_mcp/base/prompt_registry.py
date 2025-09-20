"""
Prompt注册器
负责将Prompt操作注册为MCP prompts
"""
from typing import Dict, Type, List
from ..prompts.base_prompt import BasePrompt
from .models import PromptResult
from fastmcp import FastMCP


class PromptRegistry:
    """Prompt注册器"""
    
    def __init__(self, mcp_server: FastMCP):
        self.mcp_server = mcp_server
        self.prompts: Dict[str, BasePrompt] = {}
    
    def register(self, prompt_class: Type[BasePrompt]) -> None:
        """注册一个Prompt操作"""
        prompt = prompt_class()
        self.prompts[prompt.name] = prompt
        
        # 获取输入模型的字段信息
        input_model = prompt.arguments_schema
        
        # 使用 exec 动态创建具有明确参数的prompt函数
        def create_prompt_function():
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
async def prompt_function({params_str}):
    try:
        kwargs = {{{kwargs_str}}}
        input_data = input_model(**kwargs)
        return await prompt.generate(input_data)
    except Exception as e:
        return PromptResult(
            success=False,
            content="",
            error_message=str(e),
            prompt_name=prompt.name
        )
"""
            
            # 执行代码创建函数
            local_vars = {
                'input_model': input_model,
                'prompt': prompt,
                'PromptResult': PromptResult,
                'List': List
            }
            global_vars = {
                'input_model': input_model,
                'prompt': prompt,
                'PromptResult': PromptResult,
                'List': List
            }
            exec(func_code, global_vars, local_vars)
            prompt_function = local_vars['prompt_function']
            prompt_function.__name__ = prompt.name
            return prompt_function
        
        prompt_function = create_prompt_function()
        
        # 注册为MCP prompt
        self.mcp_server.prompt(description=prompt.description)(prompt_function)
    
    def get_prompt(self, name: str) -> BasePrompt:
        """获取指定的Prompt操作"""
        return self.prompts.get(name)
    
    def list_prompts(self) -> list[str]:
        """列出所有已注册的Prompt"""
        return list(self.prompts.keys())