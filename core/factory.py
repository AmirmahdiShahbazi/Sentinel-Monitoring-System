import json
from typing import Dict, Type
from core.base import BaseCheck, BaseAlert
from plugins.checks import HttpCheck, SystemCheck
from plugins.alerts import ConsoleAlert, LogAlert

class Factory:

    ALERT_REGISTRY: Dict[str, Type[BaseAlert]] = {
        "console": ConsoleAlert,
        "log": LogAlert
    }

    CHECK_REGISTRY: Dict[str, Type[BaseCheck]] = {
        "http": HttpCheck,
        "system": SystemCheck
    }

    @classmethod
    def create_check(cls, check_data: dict) -> BaseCheck:
        check_type = check_data["type"]
        class_obj = cls.CHECK_REGISTRY.get(check_type)
        
        if not class_obj:
            raise ValueError(f"Unknown check type: {check_type}")
        
        return class_obj(name=check_data["name"], **check_data["params"])

    @classmethod
    def create_alert(cls, alert_data: dict) -> BaseAlert:
        alert_type = alert_data["type"]
        class_obj = cls.ALERT_REGISTRY.get(alert_type)
        
        if not class_obj:
            raise ValueError(f"Unknown alert type: {alert_type}")
            
        return class_obj()