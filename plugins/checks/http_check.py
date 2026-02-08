import httpx
import time
from core.base import BaseCheck, CheckResult

class HttpCheck(BaseCheck):
    def __init__(self, name: str, url: str):
        super().__init__(name)
        self.url = url
    
    async def run(self) -> CheckResult:
        start_time = time.perf_counter()
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.url, timeout=5.0)
                
                end_time = time.perf_counter() - start_time
                
                if response.status_code == 200:
                    return CheckResult(
                        name=self.name,
                        status=True,
                        message="Website is healthy",
                        response_time=round(end_time, 3)
                    )
                else:
                    return CheckResult(
                        name=self.name,
                        status=False,
                        message=f"Server returned status {response.status_code}",
                        response_time=round(end_time, 3)
                    )

            except Exception as e:
                return CheckResult(
                    name=self.name,
                    status=False,
                    message=f"Connection failed: {str(e)}"
                )