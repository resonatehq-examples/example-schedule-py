"""
Run this script to start processing scheduled executions.
The worker polls the Resonate server for tasks created by the scheduler.
"""
import signal
from threading import Event
from resonate import Resonate
from report import generate_report

resonate = Resonate(url="http://localhost:8001")
resonate.register(generate_report)

stop_event = Event()

def shutdown(sig, frame):
    resonate.stop()
    stop_event.set()

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

print("Worker started. Waiting for scheduled executions...")
resonate.start()
stop_event.wait()
