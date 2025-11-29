import csv, json
from datetime import datetime, timedelta
from db.mongo import get_db
import asyncio

async def generate_report():
    db = get_db()
    since = datetime.utcnow() - timedelta(days=1)
    changes = await db.change_logs.find({"timestamp": {"$gte": since}}).to_list(None)

    date = datetime.utcnow().strftime("%Y-%m-%d")

    # JSON
    with open(f"reports/change_report_{date}.json", "w") as f:
        json.dump(changes, f, default=str, indent=2)

    # CSV
    with open(f"reports/change_report_{date}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "source_url", "field", "old", "new"])

        for c in changes:
            ch = c["change"]
            writer.writerow([c["timestamp"], c["source_url"], ch["field"], ch["old"], ch["new"]])

    print(f"Report generated for {date}")

if __name__ == "__main__":
    asyncio.run(generate_report())
