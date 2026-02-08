import asyncio
from typing import List
from core.base import BaseCheck, BaseAlert
from plugins.checks import HttpCheck 

class MonitorEngine:
    def __init__(self):
        self.checks: List[BaseCheck] = []
        self.alerts: List[BaseAlert] = []
        self.results_cache: Dict[str, any] = {}

    def add_check(self, check: BaseCheck):
        self.checks.append(check)
        self.results_cache[check.name] = None

    def add_alert(self, alert: BaseAlert):
        self.alerts.append(alert)
        
    async def run_check(self, check: BaseCheck):
        """Runs a single check and triggers alerts if it fails."""
        result = await check.run()

        self.results_cache[check.name] = result

        for alert in self.alerts:
            await alert.handle(result)


    async def run_all(self):
        """The main loop that runs everything once."""
        tasks = [self.run_check(c) for c in self.checks]
        await asyncio.gather(*tasks)
