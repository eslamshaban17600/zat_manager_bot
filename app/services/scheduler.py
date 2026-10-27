import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from aiogram import Bot
from app.core.config import settings
from app.core.logging_config import logger
from app.database.session import AsyncSessionLocal
from app.database.models import ScheduledJobModel
from sqlalchemy import select

# إعداد مخزن المهام في قاعدة البيانات لضمان عدم ضياعها عند إعادة التشغيل
jobstores = {
    'default': SQLAlchemyJobStore(url=settings.DB_URL.replace("aiosqlite", "sqlite"))
}

scheduler = AsyncIOScheduler(jobstores=jobstores, timezone=settings.TIMEZONE)

async def scheduled_message_job(bot: Bot, channel_id: str, text: str):
    """
    الدالة التي يتم تنفيذها تلقائياً عند حلول موعد المهمة المجدولة.
    """
    try:
        await bot.send_message(chat_id=channel_id, text=text, parse_mode="HTML")
        logger.info(f"تم تنفيذ المهمة المجدولة بنجاح وإرسال الرسالة إلى القناة {channel_id}")
    except Exception as e:
        logger.error(f"فشل تنفيذ المهمة المجدولة للقناة {channel_id}: {e}")

def add_interval_job(job_id: str, channel_id: str, text: str, bot: Bot, hours: int = 24):
    """
    إضافة مهمة متكررة كل عدد معين من الساعات.
    """
    scheduler.add_job(
        scheduled_message_job,
        'interval',
        hours=hours,
        args=[bot, channel_id, text],
        id=job_id,
        replace_existing=True
    )
    logger.info(f"تمت جدولة مهمة متكررة للقناة {channel_id} كل {hours} ساعة برقم {job_id}")

def add_date_job(job_id: str, channel_id: str, text: str, bot: Bot, run_date: datetime.datetime):
    """
    إضافة مهمة تُنفذ مرة واحدة في تاريخ ووقت محددين.
    """
    scheduler.add_job(
        scheduled_message_job,
        'date',
        run_date=run_date,
        args=[bot, channel_id, text],
        id=job_id,
        replace_existing=True
    )
    logger.info(f"تمت جدولة مهمة لمرة واحدة للقناة {channel_id} في موعد {run_date}")

def init_scheduler(bot: Bot):
    try:
        if not scheduler.running:
            scheduler.start()
            logger.info("تم تشغيل محرك الجدولة (APScheduler) واستعادة كافة المهام بنجاح.")
    except Exception as e:
        logger.error(f"خطأ أثناء تشغيل محرك الجدولة: {e}")