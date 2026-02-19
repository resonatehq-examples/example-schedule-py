"""
Run this script once to create the schedule.
The Resonate server will trigger `generate_report` according to the cron expression.
"""
from resonate import Resonate
from resonate.errors.errors import ResonateStoreError
from report import generate_report

resonate = Resonate(url="http://localhost:8001")
resonate.register(generate_report)

try:
    # Schedule generate_report to run every minute
    resonate.schedule(
        "daily_report",   # schedule ID
        generate_report,  # function to run
        "* * * * *",      # cron: every minute (change to "0 9 * * *" for daily at 9am)
        user_id=123,      # arguments
    )
    print("Schedule created. Start the worker to process executions.")
except ResonateStoreError as e:
    if e.code == 100.40901:
        print("Schedule already exists. Start the worker to process executions.")
    else:
        raise
