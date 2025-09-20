"""
Prompt基类定义
定义所有Prompt的统一接口和抽象方法
"""
from abc import ABC, abstractmethod
from typing import Any, Type
from pydantic import BaseModel
from ..base.models import PromptResult


class BasePrompt(ABC):
    """所有Prompt的基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Prompt名称"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Prompt描述"""
        pass
    
    @property
    @abstractmethod
    def arguments_schema(self) -> Type[BaseModel]:
        """参数模式"""
        pass
    
    @abstractmethod
    async def generate(self, arguments: BaseModel) -> PromptResult:
        """生成Prompt内容"""
        pass
    
    @abstractmethod
    def validate_arguments(self, arguments: Any) -> bool:
        """验证参数有效性"""
        pass