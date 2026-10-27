from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from app.bot.states.channel_states import ChannelAddStates
from app.services.channels import verify_and_add_channel, get_all_channels
from app.bot.keyboards.main_menu import get_back_to_main_keyboard

router = Router()

@router.callback_query(F.data == "menu_channels")
async def channels_management_menu(callback: CallbackQuery):
    channels = await get_all_channels()
    
    channels_text = "📢 **إدارة القنوات الإسلامية:**\n\n"
    if channels:
        channels_text += "القنوات المسجلة حالياً:\n"
        for idx, ch in enumerate(channels, 1):
            status = "🟢 مفعلة" if ch.is_active else "🔴 متوقفة"
            username_str = f" (@{ch.username})" if ch.username else ""
            channels_text += f"{idx}. **{ch.title}**{username_str} - {status}\n"
    else:
        channels_text += "لا توجد قنوات مسجلة حتى الآن.\n"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ إضافة قناة جديدة", callback_data="add_channel_start")],
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])

    await callback.message.edit_text(channels_text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "add_channel_start")
async def start_add_channel(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChannelAddStates.waiting_for_channel_input)
    
    cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ إلغاء", callback_data="menu_channels")]
    ])
    
    text = (
        "➕ **إضافة قناة جديدة:**\n\n"
        "الرجاء إرسال معرف القناة (مثال: `@my_channel`) أو رابط الدعوة، أو الـ ID الخاص بالقناة.\n\n"
        "⚠️ **ملاحظة هامة:** يجب التأكد من إضافة البوت مشرفاً في القناة مع منح صلاحية **نشر الرسائل** أولاً."
    )
    await callback.message.edit_text(text, reply_markup=cancel_kb, parse_mode="Markdown")
    await callback.answer()

@router.message(ChannelAddStates.waiting_for_channel_input)
async def process_channel_input(message: Message, state: FSMContext, bot: Bot):
    channel_input = message.text.strip()
    
    processing_msg = await message.answer("🔄 جاري التحقق من القناة وصلاحيات البوت...")

    success, response_message = await verify_and_add_channel(bot, channel_input, message.from_user.id)
    
    await processing_msg.delete()
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 العودة لإدارة القنوات", callback_data="menu_channels")],
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])

    await message.answer(response_message, reply_markup=keyboard, parse_mode="Markdown")
    await state.clear()