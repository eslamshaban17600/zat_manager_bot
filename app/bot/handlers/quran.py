from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.services.quran_audio import get_all_reciters

router = Router()

@router.callback_query(F.data == "menu_quran")
async def quran_audio_menu(callback: CallbackQuery):
    reciters = await get_all_reciters()
    
    text = "📖 **نظام الختمات السماعية للقرآن الكريم:**\n\n"
    if reciters:
        text += "القراء المتاحون في النظام:\n"
        for idx, r in enumerate(reciters, 1):
            text += f"{idx}. **{r.display_name}**\n"
    else:
        text += "لا توجد قراء مسجلون حالياً في قاعدة البيانات.\n"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎧 إدارة خطط الختم", callback_data="listening_plans")],
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()