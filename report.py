from datetime import datetime
from resonate import Context


def generate_report(ctx: Context, user_id: int) -> str:
    timestamp = datetime.utcnow().isoformat()
    report = f"[{timestamp}] Report for user {user_id}"
    print(report)
    return report
