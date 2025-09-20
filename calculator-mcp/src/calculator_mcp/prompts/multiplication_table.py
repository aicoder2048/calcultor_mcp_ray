"""
乘法口诀表Prompt实现
生成指导Claude使用multiplication工具创建乘法口诀表的文本
"""
from typing import Type
from pydantic import BaseModel, Field, field_validator
from .base_prompt import BasePrompt
from ..base.models import PromptResult


class MultiplicationTableArguments(BaseModel):
    """乘法口诀表参数模型"""
    size: int = Field(..., description="口诀表大小", ge=1, le=20)
    start_number: int = Field(1, description="起始数字", ge=-100, le=100)
    language: str = Field("zh", description="输出语言: zh(中文) 或 en(英文)")
    format: str = Field("table", description="输出格式: table(表格) 或 list(列表)")
    
    @field_validator('language')
    @classmethod
    def validate_language(cls, v):
        if v not in ['zh', 'en']:
            raise ValueError('语言必须是 "zh" 或 "en"')
        return v
    
    @field_validator('format')
    @classmethod
    def validate_format(cls, v):
        if v not in ['table', 'list']:
            raise ValueError('格式必须是 "table" 或 "list"')
        return v


class MultiplicationTablePrompt(BasePrompt):
    """乘法口诀表Prompt实现"""
    
    @property
    def name(self) -> str:
        return "multiplication_table"
    
    @property
    def description(self) -> str:
        return "生成自定义大小和起始数字的乘法口诀表，支持中英文输出和多种格式"
    
    @property
    def arguments_schema(self) -> Type[BaseModel]:
        return MultiplicationTableArguments
    
    def validate_arguments(self, arguments: MultiplicationTableArguments) -> bool:
        """验证参数有效性"""
        try:
            # 检查大小范围
            if not (1 <= arguments.size <= 20):
                return False
            
            # 检查起始数字范围
            if not (-100 <= arguments.start_number <= 100):
                return False
            
            # 检查计算结果不会溢出
            max_result = (arguments.start_number + arguments.size - 1) ** 2
            if abs(max_result) > 1e15:  # 防止计算结果过大
                return False
            
            return True
        except Exception:
            return False
    
    async def generate(self, arguments: MultiplicationTableArguments) -> PromptResult:
        """生成乘法口诀表Prompt文本"""
        if not self.validate_arguments(arguments):
            return PromptResult(
                success=False,
                content="",
                error_message="参数验证失败：大小必须在1-20之间，起始数字必须在-100到100之间",
                prompt_name=self.name
            )
        
        try:
            # 生成引导Claude使用multiplication工具的prompt文本
            if arguments.language == "zh":
                prompt_content = self._generate_chinese_prompt(arguments)
            else:
                prompt_content = self._generate_english_prompt(arguments)
            
            return PromptResult(
                success=True,
                content=prompt_content,
                prompt_name=self.name,
                metadata={
                    "size": arguments.size,
                    "start_number": arguments.start_number,
                    "language": arguments.language,
                    "format": arguments.format
                }
            )
            
        except Exception as e:
            return PromptResult(
                success=False,
                content="",
                error_message=f"生成乘法口诀表Prompt失败: {str(e)}",
                prompt_name=self.name
            )
    
    def _generate_chinese_prompt(self, args: MultiplicationTableArguments) -> str:
        """生成中文指导prompt"""
        format_instruction = "表格格式" if args.format == "table" else "列表格式"
        
        prompt = f"""请帮我创建一个{args.size}x{args.size}的乘法口诀表，起始数字为{args.start_number}，使用{format_instruction}输出。

具体要求：
1. 使用multiplication工具计算每个乘法运算
2. 从{args.start_number}开始，到{args.start_number + args.size - 1}结束
3. 计算所有可能的乘法组合：{args.start_number}×{args.start_number}, {args.start_number}×{args.start_number + 1}, ... {args.start_number + args.size - 1}×{args.start_number + args.size - 1}

输出格式要求：
"""
        
        if args.format == "table":
            prompt += f"""- 使用表格格式展示
- 第一行显示标题：乘法口诀表 ({args.size}x{args.size}, 起始数字: {args.start_number})
- 创建行列标题显示乘数和被乘数
- 在表格中填入每个位置的乘法结果"""
        else:
            prompt += f"""- 使用列表格式展示  
- 第一行显示标题：乘法口诀表 ({args.size}x{args.size}, 起始数字: {args.start_number})
- 每行显示一个乘法算式：数字1 × 数字2 = 结果
- 按照从小到大的顺序排列"""
        
        prompt += f"""

请使用multiplication工具逐个计算每个乘法运算，确保结果准确。总共需要计算{args.size * args.size}个乘法运算。"""
        
        return prompt
    
    def _generate_english_prompt(self, args: MultiplicationTableArguments) -> str:
        """生成英文指导prompt"""
        format_instruction = "table format" if args.format == "table" else "list format"
        
        prompt = f"""Please help me create a {args.size}x{args.size} multiplication table starting from {args.start_number}, using {format_instruction} output.

Requirements:
1. Use the multiplication tool to calculate each multiplication operation
2. Start from {args.start_number} and end at {args.start_number + args.size - 1}
3. Calculate all possible multiplication combinations: {args.start_number}×{args.start_number}, {args.start_number}×{args.start_number + 1}, ... {args.start_number + args.size - 1}×{args.start_number + args.size - 1}

Output format requirements:
"""
        
        if args.format == "table":
            prompt += f"""- Display in table format
- First line shows title: Multiplication Table ({args.size}x{args.size}, Starting from: {args.start_number})
- Create row and column headers showing multiplicands
- Fill in multiplication results in each position"""
        else:
            prompt += f"""- Display in list format
- First line shows title: Multiplication Table ({args.size}x{args.size}, Starting from: {args.start_number})
- Each line shows one multiplication equation: number1 × number2 = result
- Arrange in ascending order"""
        
        prompt += f"""

Please use the multiplication tool to calculate each multiplication operation individually to ensure accurate results. Total of {args.size * args.size} multiplication operations needed."""
        
        return prompt