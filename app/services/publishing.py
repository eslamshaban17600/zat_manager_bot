from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from app.core.logging_config import logger

async def send_instant_post(bot: Bot, channel_id: str, text: str, parse_mode: str = "HTML") -> tuple[bool, str]:
    """
    إرسال منشور فوري إلى القناة المستهدفة مع معالجة الأخطاء والتنسيق.
    """
    try:
        await bot.send_message(
            chat_id=channel_id,
            text=text,
            parse_mode=parse_mode
        )
        logger.info(f"تم إرسال المنشور بنجاح إلى القناة {channel_id}")
        return True, "✅ تم نشر الرسالة بنجاح في القناة المستهدفة!"
    except TelegramAPIError as e:
        logger.error(f"خطأ في إرسال المنشور إلى {channel_id}: {e}")
        return False, f"❌ فشل النشر بسبب خطأ من تيليجرام: {str(e)}"
    except Exception as e:
        logger.error(f"خطأ غير متوقع أثناء النشر: {e}")
        return False, f"❌ حدث خطأ تقني غير متوقع: {str(e)}"