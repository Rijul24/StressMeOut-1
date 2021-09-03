import os
import pytz

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

LOGGING_CHANNEL_ID = 883049245421236247

BOT_INVITE = ""
GITHUB_LINK = "https://github.com/armaanbadhan/StressMeOut"

# doesnt work for some reason?
OWNERS = [762615112385036288, 786851962833862676]

TOKEN = os.getenv('TOKEN')

SQLITE_LOCATION = "/jobs.sqlite"


# scheduler
jobstores = {
    "default": SQLAlchemyJobStore(url=f"sqlite://{SQLITE_LOCATION}")
}
job_defaults = {
    "coalesce": True
}
scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    timezone=pytz.timezone("Asia/Kolkata"),
    job_defaults=job_defaults,
)
