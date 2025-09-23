"""
质数判断操作
判断一个数是否为质数
"""
import math
from typing import Type
from pydantic import BaseModel, Field
from ..base.operation import BaseOperation
from ..base.models import OperationResult


class PrimeCheckInput(BaseModel):
    number: int = Field(..., description="待判断的整数", gt=1)


class PrimeCheckOperation(BaseOperation):
    
    @property
    def name(self) -> str:
        return "prime_check"
    
    @property
    def description(self) -> str:
        return "判断一个整数是否为质数(素数)"
    
    @property
    def input_model(self) -> Type[BaseModel]:
        return PrimeCheckInput
    
    def validate_input(self, input_data: PrimeCheckInput) -> bool:
        if input_data.number <= 1:
            return False
        if input_data.number > 10**15:
            return False
        return True
    
    def _is_prime(self, n: int) -> bool:
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        
        return True
    
    def _find_factors(self, n: int, max_factors: int = 10) -> list:
        factors = []
        for i in range(2, min(int(math.sqrt(n)) + 1, 10000)):
            if n % i == 0:
                factors.append(i)
                if len(factors) >= max_factors:
                    break
        return factors
    
    async def execute(self, input_data: PrimeCheckInput) -> OperationResult:
        if not self.validate_input(input_data):
            if input_data.number <= 1:
                error_msg = "质数判断只适用于大于1的整数"
            else:
                error_msg = "数值过大(最大支持10^15), 请使用更小的值"
            
            return OperationResult(
                success=False,
                result=0,
                error_message=error_msg,
                operation_name=self.name
            )
        
        try:
            is_prime = self._is_prime(input_data.number)
            
            factors = []
            if not is_prime:
                factors = self._find_factors(input_data.number, max_factors=10)
            
            return OperationResult(
                success=True,
                result=1.0 if is_prime else 0.0,
                operation_name=self.name,
                metadata={
                    "number": input_data.number,
                    "is_prime": is_prime,
                    "result_text": "是质数" if is_prime else "不是质数",
                    "factors": factors if not is_prime else [],
                    "factor_count": len(factors) if not is_prime else 0,
                    "explanation": f"{input_data.number}是质数" if is_prime else f"{input_data.number}不是质数, 因数包括: {factors[:5]}" + ("..." if len(factors) > 5 else "")
                }
            )
            
        except Exception as e:
            return OperationResult(
                success=False,
                result=0,
                error_message=f"质数判断失败: {str(e)}",
                operation_name=self.name
            )