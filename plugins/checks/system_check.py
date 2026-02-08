import psutil
from core.base import BaseCheck, CheckResult

class SystemCheck(BaseCheck):
    def __init__(self, name: str, cpu_threshold: int = 80, ram_threshold: int = 80):
        super().__init__(name)
        self.cpu_threshold = cpu_threshold
        self.ram_threshold = ram_threshold

    async def run(self) -> CheckResult:
        cpu_usage = psutil.cpu_percent(interval=None)
        ram_usage = psutil.virtual_memory().percent
        
        message = f"CPU: {cpu_usage}% | RAM: {ram_usage}%"
        
        is_healthy = cpu_usage < self.cpu_threshold and ram_usage < self.ram_threshold
        
        status_msg = "System Healthy" if is_healthy else "Resource Threshold Exceeded!"
        
        return CheckResult(
            name=self.name,
            status=is_healthy,
            message=f"{status_msg} ({message})"
        )