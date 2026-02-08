# Sentinel Monitoring System

Sentinel is a lightweight, asynchronous Python monitoring framework with a pluggable checks-and-alerts architecture and a terminal dashboard. It ships with HTTP and system checks, and includes console and file-based alert handlers. Designed to be easy to extend and operate.

---

## Features
- Periodic execution of checks (configured interval)
- HTTP checks (with response time measurement)
- System checks (CPU/RAM thresholds)
- Alerting to console and to a rotating file (logger)
- Live terminal dashboard with status, response time, and last message

---

## Requirements
- Python 3.10+ recommended
- Git (optional)
- System packages: none required beyond Python
- Python packages (see `requirements.txt`):
  - anyio, httpx, psutil, rich, etc.

Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Quick start

1. Clone (or copy) the repo and install requirements (see above).
2. Edit `config.json` to suit your environment (example below).
3. Run:
```bash
python main.py
```

The program will:
- Load `config.json`
- Instantiate checks and alerts via `core.factory.Factory`
- Start the engine loop which runs checks concurrently
- Show a live terminal dashboard via `core.dashboard.Dashboard`

Press Ctrl+C to stop.

---

## Configuration

The runtime configuration lives in `config.json`. Example:
```json
{
  "settings": {
    "interval": 10
  },
  "checks": [
    {
      "type": "http",
      "name": "Google",
      "params": { "url": "https://www.google.com" }
    },
    {
      "type": "system",
      "name": "Local Server",
      "params": { "cpu_threshold": 90, "ram_threshold": 85 }
    }
  ],
  "alerts": [
    { "type": "log" }
  ]
}
```

- settings.interval: seconds to wait between runs in `main.py`. The loop: run all checks → update dashboard → sleep interval.
- checks: list of check items. Each has:
  - type: one of `http`, `system` (see Factory.CHECK_REGISTRY)
  - name: friendly display name
  - params: check-specific parameters
- alerts: list of alert items. Each has:
  - type: one of `console`, `log` (see Factory.ALERT_REGISTRY)
  - alert-specific params (currently `LogAlert` accepts optional filename when constructed programmatically; config->Factory currently constructs alerts without params)

Built-in checks:
- http: requires `url` param. Measures response time and checks for HTTP 200.
- system: optional `cpu_threshold` and `ram_threshold` numbers (percentages).

Built-in alerts:
- console: prints status lines to stdout
- log: appends failure entries to `sentinel_errors.log` (default filename; see LogAlert initializer)

---

## Components & Architecture

High-level flow:
main.py -> Factory -> MonitorEngine -> (checks run concurrently) -> Alerts -> Dashboard (rich Live)

Roles:
- main.py: orchestrates startup, loads config and creates engine/dashboard, enters run loop.
- core.factory.Factory: maps string type names to concrete classes and constructs them.
- core.engine.MonitorEngine: keeps check and alert lists, runs checks concurrently with asyncio.gather and forwards each CheckResult to all alerts.
- core.base:
  - CheckResult dataclass (name, status, message, timestamp, response_time)
  - BaseCheck: contract for checks (async run -> CheckResult)
  - BaseAlert: contract for alerts (async handle(result))
- plugins/checks: concrete checks (HttpCheck, SystemCheck)
- plugins/alerts: concrete alerts (ConsoleAlert, LogAlert)
- core.dashboard.Dashboard: draws and updates the console UI using rich.Live and a Table.

Concurrency model:
- Each check implements an async run(). MonitorEngine schedules all checks concurrently each cycle:
  tasks = [self.run_check(c) for c in self.checks]
  await asyncio.gather(*tasks)

Every check result is forwarded to every alert by calling alert.handle(result) (async). Alerts must be implemented as async to avoid blocking the loop.

---

## Extending Sentinel

### Add a new check
1. Create a new file in `plugins/checks`, e.g. `plugins/checks/ping_check.py`:
```python
# plugins/checks/ping_check.py
from core.base import BaseCheck, CheckResult
import asyncio
import time

class PingCheck(BaseCheck):
    def __init__(self, name: str, host: str, timeout: float = 1.0):
        super().__init__(name)
        self.host = host
        self.timeout = timeout

    async def run(self) -> CheckResult:
        start = time.perf_counter()
        try:
            # Replace with a proper async ping or socket probe
            await asyncio.sleep(0.01)  # placeholder
            elapsed = round(time.perf_counter() - start, 3)
            return CheckResult(name=self.name, status=True, message=f"{self.host} reachable", response_time=elapsed)
        except Exception as e:
            return CheckResult(name=self.name, status=False, message=str(e))
```

2. Register the check in `core/factory.py`:
```python
from plugins.checks.ping_check import PingCheck

Factory.CHECK_REGISTRY["ping"] = PingCheck
```

3. Add to `config.json`:
```json
{ "type": "ping", "name": "Local Host", "params": { "host": "127.0.0.1" } }
```

### Add a new alert
1. Create `plugins/alerts/slack_alert.py`:
```python
# plugins/alerts/slack_alert.py
from core.base import BaseAlert, CheckResult
import httpx

class SlackAlert(BaseAlert):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def handle(self, result: CheckResult):
        if not result.status:
            # send a simple message
            async with httpx.AsyncClient() as client:
                await client.post(self.webhook_url, json={"text": f"{result.name} failed: {result.message}"})
```

2. Register it in `core/factory.py`:
```python
from plugins.alerts.slack_alert import SlackAlert

Factory.ALERT_REGISTRY["slack"] = SlackAlert
```

Note: Factory currently constructs alerts without parameters from config. To support alert params via JSON, modify `Factory.create_alert` to pass `alert_data.get("params", {})` (example provided below).

---

## Practical Examples

- Running the app:
```bash
python main.py
```

- Example alert from ConsoleAlert:
```
[✅ SUCCESS] Google: Website is healthy (0.123s)
[❌ FAILURE] Broke API: Connection failed: <error message> (0s)
```

- Example logged error (sentinel_errors.log):
```
2026-01-01 12:00:00,000 - ERROR - Check 'Broke API' failed: Connection failed: <error message>
```

## Contributing
Contributions are welcome! Typical workflow:
- Fork -> branch -> PR with tests and description.
- Make sure code style is consistent and add docs for new features.
- If adding checks/alerts, please include example config entries and small usage notes.

---
