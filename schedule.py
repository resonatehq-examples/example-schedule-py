"""
Run this script once to create the schedule.
The Resonate server will trigger `generate_report` according to the cron expression.
"""
from __future__ import annotations

import asyncio
import os

from resonate.error import ServerError
from resonate.resonate import Resonate

from report import generate_report


async def main() -> None:
    r = Resonate(url=os.environ.get("RESONATE_URL", "http://localhost:8001"))
    r.register(generate_report)

    # Yield to the event loop so the SDK's internal network start task
    # (queued via asyncio.create_task in Resonate.__init__) has a chance
    # to run before the first send() call checks the running flag.
    await asyncio.sleep(0)

    try:
        # Schedule generate_report to run every minute
        await r.schedule(
            id="daily_report",
            cron="* * * * *",          # every minute (change to "0 9 * * *" for daily at 9am)
            func_name="generate_report",
            args=(123,),               # user_id
            kwargs={},
        )
        print("Schedule created. Start the worker to process executions.")
    except ServerError as e:
        if e.code == 409:
            print("Schedule already exists. Start the worker to process executions.")
        else:
            raise
    finally:
        await r.stop()


if __name__ == "__main__":
    asyncio.run(main())
