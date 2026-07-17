"""
Run this script once to create the schedule.
The Resonate server will trigger `generate_report` according to the cron expression.
"""
from __future__ import annotations

import asyncio
import os

from resonate.resonate import Resonate

from report import generate_report


async def main() -> None:
    r = Resonate(url=os.environ.get("RESONATE_URL", "http://localhost:8001"))
    r.register(generate_report)

    # Yield to the event loop once so the SDK's background network task starts
    # before the first client call -- on resonate-sdk 0.7.x the first awaited
    # call otherwise fails with "http error: network has been stopped".
    # Drop this once resonatehq/resonate-sdk-py#443 is fixed.
    await asyncio.sleep(0)

    try:
        # Schedule generate_report to run every minute.
        # Re-running this script is a no-op once the schedule exists.
        await r.schedule(
            id="daily_report",
            cron="* * * * *",          # every minute (change to "0 9 * * *" for daily at 9am UTC)
            func_name="generate_report",
            args=(123,),               # user_id
        )
        print("Schedule registered. Start the worker to process executions.")
    finally:
        await r.stop()


if __name__ == "__main__":
    asyncio.run(main())
