from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.database.models import AdminModel
from app.core.config import settings

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user = event.from_user
        if not user:
            return

        # السماح لمالك النظام المحدد في ملف البيئة تلقائياً
        if user.id == settings.OWNER_USER_ID:
            return await handler(event, data)

        # التحقق من قاعدة البيانات للإداريين المصرح لهم
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(AdminModel).where(AdminModel.user_id == user.id)
            )
            admin = result.scalar_one_or_none()
            if admin:
                return await handler(event, data)

        # إذا لم يكن مصرحاً له
        if isinstance(event, Message):
            await event.answer("⚠️ عذراً، لست مصرحاً لك بالاستخدام الإداري لهذا البوت.")
        elif isinstance(event, CallbackQuery):
            await event.answer("⚠️ عذراً، غير مصرح.", show_alert=True)
        return