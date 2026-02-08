import asyncio
import json
from core.engine import MonitorEngine
from core.factory import Factory
from core.dashboard import Dashboard

async def main():
    # 1. Setup Engine
    engine = MonitorEngine()

    # 2. Load Config & Populate
    with open("config.json", "r") as f:
        config = json.load(f)

    interval = config.get("settings", {}).get("interval", 10)

    for a_data in config["alerts"]:
        engine.add_alert(Factory.create_alert(a_data))

    for c_data in config["checks"]:
        engine.add_check(Factory.create_check(c_data))

    # 3. Setup Dashboard
    db = Dashboard(engine)

    # 4. Run the loop
    with db.get_live_display() as live:
        while True:
            await engine.run_all()
            
            live.update(db.generate_table())
            
            await asyncio.sleep(interval)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Sentinel stopped by user.")