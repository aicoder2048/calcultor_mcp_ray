"""
Prompt注册器
负责将Prompt操作注册为MCP prompts
"""
from typing import Dict, Type, List, Optional, Union, get_origin, get_args
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
            
            # 创建参数列表和docstring的Args部分
            params = []
            docstring_args = []
            
            for field_name, field_info in fields.items():
                # 获取类型注解
                field_type = field_info.annotation
                
                # 处理Optional类型
                origin = get_origin(field_type)
                if origin is Union:
                    # 这是一个Union类型，检查是否是Optional（即Union[X, None]）
                    args = get_args(field_type)
                    if len(args) == 2 and type(None) in args:
                        # 这是Optional[X]
                        inner_type = args[0] if args[1] is type(None) else args[1]
                        if hasattr(inner_type, '__name__'):
                            type_name = f"Optional[{inner_type.__name__}]"
                        else:
                            type_name = f"Optional[{str(inner_type)}]"
                    else:
                        type_name = str(field_type)
                elif hasattr(field_type, '__name__'):
                    type_name = field_type.__name__
                else:
                    type_name = str(field_type)
                
                # 处理默认值
                if field_info.is_required():
                    params.append(f"{field_name}: {type_name}")
                else:
                    default_value = field_info.get_default()
                    if default_value is None:
                        params.append(f"{field_name}: {type_name} = None")
                    elif isinstance(default_value, str):
                        params.append(f"{field_name}: {type_name} = '{default_value}'")
                    else:
                        params.append(f"{field_name}: {type_name} = {default_value}")
                
                # 为docstring创建参数描述
                arg_description = field_info.description or f"{field_name} parameter"
                docstring_args.append(f"        {field_name}: {arg_description}")
            
            params_str = ', '.join(params)
            
            # 创建完整的docstring
            docstring = f'''"""{prompt.description}
    
    Args:
{chr(10).join(docstring_args)}
    """'''
            
            # 创建kwargs字符串 - 需要处理可选参数和必需参数
            kwargs_creation = []
            for field_name, field_info in fields.items():
                if field_info.is_required():
                    # 必需参数直接添加
                    kwargs_creation.append(f"        kwargs['{field_name}'] = {field_name}")
                else:
                    # 可选参数只在非None时添加
                    kwargs_creation.append(f"        if {field_name} is not None: kwargs['{field_name}'] = {field_name}")
            kwargs_lines = '\n'.join(kwargs_creation) if kwargs_creation else "        pass"
            
            # 动态创建函数代码，包含docstring
            func_code = f"""
async def prompt_function({params_str}):
    {docstring}
    try:
        kwargs = {{}}
{kwargs_lines}
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
            
            # 调试：打印生成的代码
            # print(f"Generated function for {prompt.name}:\n{func_code}")
            
            # 执行代码创建函数
            local_vars = {
                'input_model': input_model,
                'prompt': prompt,
                'PromptResult': PromptResult,
                'List': List,
                'Optional': Optional
            }
            global_vars = {
                'input_model': input_model,
                'prompt': prompt,
                'PromptResult': PromptResult,
                'List': List,
                'Optional': Optional
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