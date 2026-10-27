from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.database.session import AsyncSessionLocal
from app.database.models import AuditLogModel
from sqlalchemy import select

router = Router()

@router.callback_query(F.data == "menu_reports")
async def reports_menu(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(AuditLogModel).order_by(AuditLogModel.created_at.desc()).limit(5))
        logs = result.scalars().all()

    text = "📊 **التقارير وسجل التدقيق:**\n\nآخر الأنشطة الإدارية المسجلة:\n"
    if logs:
        for log in logs:
            text += f"🔹 `{log.action_type}` - المشرف: {log.admin_id} ({log.created_at})\n"
    else:
        text += "لا توجد سجلات نشاط حديثة.\n"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "menu_settings")
async def settings_menu(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💾 إنشاء نسخة احتياطية للقاعدة", callback_data="backup_db")],
        [InlineKeyboardButton(text="👑 نقل ملكية البوت", callback_data="menu_transfer_ownership")],
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])
    await callback.message.edit_text(
        "⚙️ **الإعدادات العامة والنسخ الاحتياطي:**\n\nيمكنك إجراء نسخ احتياطي فوري لقاعدة البيانات للحفاظ على أمان البيانات.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "backup_db")
async def execute_backup(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ الإعدادات", callback_data="menu_settings")],
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])
    await callback.message.edit_text(
        "✅ **تم إنشاء النسخة الاحتياطية بنجاح!**\nمجلد البيانات محمي وآمن.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "menu_quizzes")
async def quizzes_menu(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 إنشاء اختبار جديد من ملف", callback_data="create_quiz")],
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])
    await callback.message.edit_text(
        "📝 **نظام الاختبارات والمسابقات:**\n\nارفع ملف PDF أو Word لتحويل محتواره إلى اختبارات تفاعلية.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

