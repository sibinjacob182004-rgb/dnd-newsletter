from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from backend.orchestrator import run_pipeline

# Set timezone (IMPORTANT)
IST = pytz.timezone("Asia/Kolkata")

scheduler = BlockingScheduler(timezone=IST)


def start_scheduler():
    print("⏰ Scheduler started...")

    # Run daily at 8:00 AM IST
    scheduler.add_job(
        run_pipeline,
        CronTrigger(hour=8, minute=0)
    )

    scheduler.start()


if __name__ == "__main__":
    start_scheduler()