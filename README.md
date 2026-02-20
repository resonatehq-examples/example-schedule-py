# Scheduled Function | Resonate Example

Schedule a Python function to run periodically using Resonate's high-level `schedule()` API.

## What problem does this solve?

Running a function on a cron schedule sounds simple — but in practice, what happens when the worker crashes mid-execution? Traditional cron jobs offer no crash recovery: the job just doesn't run (or runs again from scratch on the next tick). Resonate makes scheduled executions durable. Each cron tick fires a new durable promise. If the worker crashes while processing it, Resonate retries automatically. No lost ticks, no manual recovery logic.

## Overview

This example shows how to use Resonate's `schedule()` method to register a function as a periodic job using a cron expression. The Resonate server triggers the function automatically, and a worker processes each execution durably.

```python
# Register the function
resonate.register(generate_report)

# Schedule it to run every minute
resonate.schedule(
    "daily_report",   # schedule ID
    generate_report,  # function to schedule
    "* * * * *",      # cron expression
    user_id=123,      # arguments
)
```

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- [Resonate server](https://docs.resonatehq.io) running locally

## Setup

### 1. Start the Resonate server

```bash
resonate dev
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Create the schedule

Run this once to register the cron schedule with the Resonate server:

```bash
uv run python schedule.py
```

### 4. Start the worker

Run the worker to process each scheduled execution:

```bash
uv run python worker.py
```

Every minute, you'll see output like:

```
[2026-02-18T09:00:00] Report for user 123
[2026-02-18T09:01:00] Report for user 123
```

## How It Works

| File | Role |
|------|------|
| `schedule.py` | Creates the cron schedule on the Resonate server (run once) |
| `worker.py` | Registers the function and polls for executions (run continuously) |
| `report.py` | The function that runs on each scheduled tick |

The Resonate server fires a new durable promise on each cron tick. The worker picks it up, executes the function, and records the result. If the worker crashes, Resonate retries the execution automatically.

## Cron Reference

| Expression | Meaning |
|------------|---------|
| `* * * * *` | Every minute |
| `0 9 * * *` | Daily at 9am |
| `0 9 * * 1-5` | Weekdays at 9am |
| `*/30 * * * *` | Every 30 minutes |

## Learn More

- [Resonate Documentation](https://docs.resonatehq.io)
- [Schedules API](https://docs.resonatehq.io/concepts/schedules)
- [Python SDK Guide](https://docs.resonatehq.io/develop/python)
