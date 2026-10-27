from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.bot.keyboards.main_menu import get_back_to_main_keyboard
from app.services.content_library import get_content_by_category

router = Router()

@router.callback_query(F.data == "menu_content_lib")
async def content_library_menu(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 القرآن والتفسير", callback_data="cat_quran")],
        [InlineKeyboardButton(text="📜 الأحاديث والفوائد", callback_data="cat_hadith")],
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])
    await callback.message.edit_text(
        "📚 **مكتبة المحتوى الإسلامي:**\n\nاختر القسم المطلوب لاستعراض المواد المحفوظة:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "menu_adhkar")
async def adhkar_menu(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌅 أذكار الصباح", callback_data="adhkar_morning")],
        [InlineKeyboardButton(text="🌆 أذكار المساء", callback_data="adhkar_evening")],
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])
    await callback.message.edit_text(
        "🌅 **قسم أذكار الصباح والمساء:**\n\nيمكنك استعراض أو جدولة أذكار الصباح والمساء بدقة:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data.in_({"adhkar_morning", "adhkar_evening"}))
async def show_adhkar_preview(callback: CallbackQuery):
    adhkar_type = "صباح" if "morning" in callback.data else "مساء"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ نشر الأذكار الآن", callback_data=f"publish_adhkar_{adhkar_type}")],
        [InlineKeyboardButton(text="↩️ رجوع للأذكار", callback_data="menu_adhkar")]
    ])
    await callback.message.edit_text(
        f"🌅 **أذكار ال{adhkar_type}:**\n\nالنظام جاهز لجلب الأذكار المسجلة في القاعدة ونشرها بشكل منسق.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()