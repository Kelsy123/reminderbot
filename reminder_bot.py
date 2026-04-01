import asyncio
import aiohttp
import os
from datetime import datetime
from zoneinfo import ZoneInfo

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
EASTERN = ZoneInfo("America/New_York")


async def send_reminder():
    payload = {
        "content": "🔔",
        "embeds": [
            {
                "title": "⏰ 5-Min Prep — 1:45 ET Incoming",
                "description": (
                    "**Mark your levels. Check your positions.**\n\n"
                    "🗓️ Potential catalysts around 1:45 PM ET (with a flexible window):\n"
                    "• Volume influx\n"
                    "• Algo triggers\n"
                    "• Pivot zones activating\n\n"
                    "Not a guarantee of movement, but always good to stay sharp."
                ),
                "color": 0xFFD700,
                "timestamp": datetime.now(EASTERN).isoformat(),
            }
        ],
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=payload) as resp:
            print(f"[{datetime.now(EASTERN)}] Reminder sent — status {resp.status}")


async def main():
    print("Bot started. Watching for 1:40 PM ET...")
    fired_today = None

    while True:
        now = datetime.now(EASTERN)
        today = now.date()

        if now.hour == 13 and now.minute == 40 and fired_today != today:
            await send_reminder()
            fired_today = today  # Prevent double-firing within the same minute

        await asyncio.sleep(20)  # Check every 20 seconds


if __name__ == "__main__":
    asyncio.run(main())
