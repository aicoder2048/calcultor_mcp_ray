"""
基础操作抽象类
定义所有数学运算的统一接口
"""
from abc import ABC, abstractmethod
from typing import Any, Type
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