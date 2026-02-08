import logging
from core.base import BaseAlert, CheckResult
from datetime import datetime

class LogAlert(BaseAlert):
    def __init__(self, filename: str = "sentinel_errors.log"):
        self.logger = logging.getLogger("SentinelLogger")
        
        if not self.logger.handlers:
            file_handler = logging.FileHandler(filename)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.logger.setLevel(logging.ERROR)

    async def handle(self, result: CheckResult):
        if not result.status:
            log_message = f"Check '{result.name}' failed: {result.message}"
            self.logger.error(log_message)