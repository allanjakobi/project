from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
from datetime import datetime

def start():
    scheduler = BackgroundScheduler()
    # Run every 3 minutes
    scheduler.add_job(
        lambda: call_command("auto_create_invoices", datetime.now().strftime("%d.%m.%Y")),
        "interval",
        minutes=3,
    )
    scheduler.add_job(
    lambda: call_command("process_issued_invoices"),
    "interval",
    minutes=3,
    )
    
    
    scheduler.start()
