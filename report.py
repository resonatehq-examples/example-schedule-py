from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from resonate.context import Context


async def generate_report(ctx: Context, user_id: int) -> str:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    report = f"[{timestamp}] Report for user {user_id}"
    print(report, flush=True)
    return report
