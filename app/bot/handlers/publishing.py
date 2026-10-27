from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from app.bot.states.publishing_states import InstantPostStates
from app.services.channels import get_all_channels
from app.services.publishing import send_instant_post

router = Router()

@router.callback_query(F.data == "menu_instant_post")
async def instant_post_menu(callback: CallbackQuery, state: FSMContext):
    channels = await get_all_channels()
    
    if not channels:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 إضافة قناة أولاً", callback_data="menu_channels")],
            [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
        ])
        await callback.message.edit_text(
            "⚠️ لا توجد أي قنوات مسجلة حالياً! يرجى إضافة قناة أولاً ليتم النشر فيها.",
            reply_markup=keyboard
        )
        await callback.answer()
        return

    # إنشاء قائمة بالأزرار للاختيار من بين القنوات المسجلة
    keyboard_buttons = []
    for ch in channels:
        if ch.is_active:
            keyboard_buttons.append([
                InlineKeyboardButton(text=f"📢 {ch.title}", callback_data=f"select_pub_ch_{ch.channel_id}")
            ])
    
    keyboard_buttons.append([InlineKeyboardButton(text="❌ إلغاء", callback_data="main_menu")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await state.set_state(InstantPostStates.waiting_for_channel_selection)
    await callback.message.edit_text(
        "✍️ **محرر النشر الفوري:**\n\nالرجاء اختيار القناة المستهدفة لنشر المحتوى:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(InstantPostStates.waiting_for_channel_selection, F.data.startswith("select_pub_ch_"))
async def channel_selected_for_post(callback: CallbackQuery, state: FSMContext):
    channel_id = callback.data.replace("select_pub_ch_", "")
    
    await state.update_data(target_channel_id=channel_id)
    await state.set_state(InstantPostStates.waiting_for_post_content)

    cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ إلغاء", callback_data="menu_instant_post")]
    ])

    await callback.message.edit_text(
        "✍️ **محرر المنشورات:**\n\n"
        "تم اختيار القناة بنجاح.\n"
        "الآن، أرسل نص المنشور الذي تود إرساله (يدعم تنسيقات HTML العادية مثل `<b>عريض</b>` أو `<i>مائل</i>`):\n\n"
        "*(أرسل النص الآن أو اضغط إلغاء للرجوع)*",
        reply_markup=cancel_kb,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.message(InstantPostStates.waiting_for_post_content)
async def receive_post_content(message: Message, state: FSMContext):
    content_text = message.text
    if not content_text:
        await message.answer("⚠️ الرجاء إرسال محتوى نصي صالح للمنشور.")
        return

    await state.update_data(post_content=content_text)
    await state.set_state(InstantPostStates.waiting_for_confirmation)

    confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ تأكيد ونشر الآن", callback_data="confirm_publish"),
            InlineKeyboardButton(text="❌ إلغاء", callback_data="main_menu")
        ]
    ])

    preview_msg = (
        "👀 **معاينة المنشور قبل النشر:**\n"
        "-----------------------------------\n"
        f"{content_text}\n"
        "-----------------------------------\n\n"
        "هل أنت متأكد من رغبتك في نشر هذا المحتوى فوراً؟"
    )
    await message.answer(preview_msg, reply_markup=confirm_kb, parse_mode="HTML")

@router.callback_query(InstantPostStates.waiting_for_confirmation, F.data == "confirm_publish")
async def execute_instant_publishing(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    channel_id = data.get("target_channel_id")
    content_text = data.get("post_content")

    await state.clear()

    processing_msg = await callback.message.edit_text("⏳ جاري نشر المحتوى في القناة...")

    success, response_msg = await send_instant_post(bot, channel_id, content_text)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ نشر منشور آخر", callback_data="menu_instant_post")],
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])

    await processing_msg.edit_text(response_msg, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()