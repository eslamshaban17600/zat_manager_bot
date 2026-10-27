from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.database.models import ChannelModel
from app.core.logging_config import logger

async def verify_and_add_channel(bot: Bot, channel_identifier: str, admin_user_id: int) -> tuple[bool, str]:
    """
    التحقق من صلاحيات البوت في القناة المراد إضافتها وحفظها في قاعدة البيانات.
    """
    try:
        # تنظيف المعرف (إزالة المسافات أو الـ @ إذا وجدت)
        clean_id = channel_identifier.strip()
        if not clean_id.startswith("@") and not clean_id.startswith("-100"):
            if clean_id.isdigit() or (clean_id.startswith("-") and clean_id[1:].isdigit()):
                clean_id = int(clean_id)
            else:
                clean_id = f"@{clean_id}"

        # جلب معلومات البوت داخل القناة
        chat = await bot.get_chat(chat_id=clean_id)
        
        if chat.type not in ["channel", "supergroup"]:
            return False, "⚠️ المعرف المدخل ليس لقناة أو مجموعة عامة صالحة."

        bot_member = await bot.get_chat_member(chat_id=chat.id, user_id=bot.id)
        
        # التحقق مما إذا كان البوت مشرفاً ويمتلك صلاحية النشر
        if bot_member.status != "administrator" or not getattr(bot_member, "can_post_messages", False):
            return False, (
                f"❌ البوت ليس مشرفاً في القناة **{chat.title}**، أو أنه لا يمتلك صلاحية **«نشر الرسائل»**.\n"
                "يرجى ترقية البوت لمشرف مع تفعيل صلاحية النشر ثم إعادة المحاولة."
            )

        # الحفظ في قاعدة البيانات
        async with AsyncSessionLocal() as session:
            # التحقق مما إذا كانت القناة مسجلة مسبقاً
            result = await session.execute(
                select(ChannelModel).where(ChannelModel.channel_id == str(chat.id))
            )
            existing_channel = result.scalar_one_or_none()

            if existing_channel:
                existing_channel.title = chat.title
                existing_channel.username = chat.username
                existing_channel.is_active = True
                await session.commit()
                return True, f"✅ تم تحديث بيانات القناة **{chat.title}** بنجاح!"

            new_channel = ChannelModel(
                channel_id=str(chat.id),
                title=chat.title,
                username=chat.username,
                is_active=True
            )
            session.add(new_channel)
            await session.commit()

        logger.info(f"تم إضافة القناة {chat.title} ({chat.id}) بواسطة المشرف {admin_user_id}")
        return True, f"✨ تمت إضافة القناة **{chat.title}** والتحقق من صلاحيات البوت بنجاح!"

    except TelegramBadRequest:
        return False, "❌ لم يتم العثور على القناة. تأكد من صحة المعرف وأن البوت مضاف فيها."
    except TelegramForbiddenError:
        return False, "❌ البوت محظور أو لا يمتلك صلاحية الوصول لهذه القناة."
    except Exception as e:
        logger.error(f"خطأ أثناء التحقق من القناة: {e}")
        return False, f"❌ حدث خطأ تقني غير متوقع: {str(e)}"

async def get_all_channels():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(ChannelModel))
        return result.scalars().all()