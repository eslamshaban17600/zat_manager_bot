from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from app.bot.states.admin_states import TransferOwnershipStates
from app.services.admin_service import transfer_bot_ownership
from app.core.config import settings

router = Router()

@router.callback_query(F.data == "menu_transfer_ownership")
async def ask_for_new_owner(callback: CallbackQuery, state: FSMContext):
    # التحقق الأمني: هل المستخدم الحالي هو المالك الأساسي المبرمج في البيئة أو المالك المسجل؟
    if callback.from_user.id != settings.OWNER_USER_ID:
        await callback.answer("⚠️ عذراً، هذه العملية مخصصة لمالك البوت الأساسي فقط!", show_alert=True)
        return

    await state.set_state(TransferOwnershipStates.waiting_for_new_owner_id)
    
    cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ إلغاء", callback_data="menu_settings")]
    ])

    text = (
        "👑 **نقل ملكية البوت:**\n\n"
        "⚠️ **تحذير خطي:** نقل الملكية سيمنح المستخدم الجديد كافة صلاحيات المالك المطلقة، ويحول صلاحيتك إلى مدير نظام عادٍ.\n\n"
        "الرجاء إرسال **Telegram User ID** الخاص بالمستخدم الجديد المراد نقل الملكية إليه:"
    )
    await callback.message.edit_text(text, reply_markup=cancel_kb, parse_mode="Markdown")
    await callback.answer()

@router.message(TransferOwnershipStates.waiting_for_new_owner_id)
async def receive_new_owner_id(message: Message, state: FSMContext):
    text_input = message.text.strip()
    
    if not text_input.isdigit():
        await message.answer("⚠️ المعرف غير صالح. يجب أن يكون رقم User ID مكوناً من أرقام فقط. حاول مجدداً أو اضغط إلغاء.")
        return

    new_owner_id = int(text_input)
    
    if new_owner_id == message.from_user.id:
        await message.answer("⚠️ لا يمكنك نقل الملكية لنفسك! أدخل معرف مستخدم آخر.")
        return

    await state.update_data(new_owner_id=new_owner_id)
    await state.set_state(TransferOwnershipStates.waiting_for_confirmation)

    confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ تأكيد نقل الملكية", callback_data="confirm_transfer_yes"),
            InlineKeyboardButton(text="❌ إلغاء", callback_data="main_menu")
        ]
    ])

    await message.answer(
        f"🔐 **تأكيد عملية نقل الملكية:**\n\n"
        f"هل أنت متأكد تماماً من رغبتك في نقل ملكية بوت **«ذآتـ 𓂆»** إلى المستخدم ذي المعرف: `{new_owner_id}`؟\n\n"
        "هذا الإجراء لا يمكن التراجع عنه بسهولة من داخل البوت مباشرة.",
        reply_markup=confirm_kb,
        parse_mode="Markdown"
    )

@router.callback_query(TransferOwnershipStates.waiting_for_confirmation, F.data == "confirm_transfer_yes")
async def execute_transfer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_owner_id = data.get("new_owner_id")
    current_owner_id = callback.from_user.id

    await state.clear()

    processing_msg = await callback.message.edit_text("🔄 جاري تحديث الصلاحيات وقاعدة البيانات وتوثيق العملية...")

    success, response_msg = await transfer_bot_ownership(current_owner_id, new_owner_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])

    await processing_msg.edit_text(response_msg, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()