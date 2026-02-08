from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CheckResult:
    """Standardized output for any check performed."""
    name: str
    status: bool  # True for Success, False for Failure
    message: str
    timestamp: datetime = datetime.now()
    response_time: float = 0.0

class BaseCheck(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def run(self) -> CheckResult:
        """
        Execute the monitoring logic. 
        Must be implemented by subclasses.
        """
        pass

class BaseAlert(ABC):
    @abstractmethod
    async def handle(self, result: CheckResult):
        """
        Define how to alert the user based on the result.
        """
        pass