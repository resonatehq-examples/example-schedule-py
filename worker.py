"""
Run this script to start processing scheduled executions.
The worker polls the Resonate server for tasks created by the scheduler.
"""
from __future__ import annotations

import asyncio
import os

from resonate.resonate import Resonate

from report import generate_report


async def main() -> None:
    r = Resonate(url=os.environ.get("RESONATE_URL", "http://localhost:8001"))
    r.register(generate_report)

    print("Worker started. Waiting for scheduled executions...", flush=True)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
