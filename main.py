import asyncio
from aiogram import Bot, Dispatcher
from app.core.config import settings
from app.core.logging_config import setup_logging, logger
from app.database.session import init_db
from app.bot.middlewares.auth import AuthMiddleware
from app.bot.handlers import start, channels, publishing, scheduler, content, quran, admin_tools,ownership
from app.services.scheduler import init_scheduler

async def main():
    # 1. إعداد السجلات
    setup_logging()
    logger.info("جاري تهيئة وتشغيل النظام المتكامل «ذآتـ 𓂆»...")

    # 2. تهيئة قاعدة البيانات والجداول
    await init_db()
    logger.info("تم إنشاء وضبط كافة جداول قاعدة البيانات بنجاح.")

    # 3. إعداد البوت والديسباتشر
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # 4. تسجيل ميدل وير الحماية والأمان
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())

    # 5. تسجيل جميع الراوترات والمتحكمات بالترتيب
    dp.include_router(start.router)
    dp.include_router(channels.router)
    dp.include_router(publishing.router)
    dp.include_router(scheduler.router)
    dp.include_router(content.router)
    dp.include_router(quran.router)
    dp.include_router(admin_tools.router)
    dp.include_router(ownership.router)

    # 6. تفعيل محرك الجدولة واستعادة المهام
    init_scheduler(bot)

    # 7. بدء استقبال التحديثات من تيليجرام
    logger.info("البوت يعمل الآن بكامل طاقته وجاهز لاستقبال التحديثات...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("تم إيقاف تشغيل البوت بواسطة المستخدم بأمان.")