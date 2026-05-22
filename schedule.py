"""
Run this script once to create the schedule.
The Resonate server will trigger `generate_report` according to the cron expression.
"""
import json
from resonate import Resonate
from resonate.errors.errors import ResonateStoreError
from report import generate_report

resonate = Resonate.remote()
resonate.register(generate_report)

# Function-call payload the worker will receive when the cron fires.
# Format matches what `resonate.options(...).rpc(...)` produces internally.
promise_data = json.dumps({
    "func": "generate_report",
    "args": [123],          # user_id
    "kwargs": {},
    "version": 1,
})

try:
    # Schedule generate_report to run every minute
    resonate.schedules.create(
        id="daily_report",
        cron="* * * * *",                       # every minute (change to "0 9 * * *" for daily at 9am)
        promise_id="daily_report.{{.timestamp}}",  # unique per cron tick
        promise_timeout=60_000,                  # 60s in ms
        promise_data=promise_data,
        promise_tags={"resonate:invoke": "poll://any@default"},
    )
    print("Schedule created. Start the worker to process executions.")
except ResonateStoreError as e:
    if e.code == 100.40901:
        print("Schedule already exists. Start the worker to process executions.")
    else:
        raise
