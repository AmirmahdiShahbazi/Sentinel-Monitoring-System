from core.base import BaseAlert, CheckResult

class ConsoleAlert(BaseAlert):
    
    async def handle(self, result: CheckResult):
        # We check the status to decide how to print
        status_label = "✅ SUCCESS" if result.status else "❌ FAILURE"
        
        print(f"[{status_label}] {result.name}: {result.message} ({result.response_time}s)")