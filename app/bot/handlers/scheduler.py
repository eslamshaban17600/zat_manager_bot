from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from app.services.channels import get_all_channels
from app.services.scheduler import scheduler

router = Router()

@router.callback_query(F.data == "menu_scheduler")
async def scheduler_menu(callback: CallbackQuery):
    jobs = scheduler.get_jobs()
    
    jobs_text = "🗓️ **نظام جدولة المنشورات:**\n\n"
    if jobs:
        jobs_text += f"عدد المهام النشطة حالياً: {len(jobs)}\n\n"
        for job in jobs:
            jobs_text += f"🔹 **مهمة ID:** `{job.id}`\n"
            jobs_text += f"   - موعد التنفيذ القادم: `{job.next_run_time}`\n\n"
    else:
        jobs_text += "لا توجد أي مهام مجدولة حالياً.\n"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ إضافة جدول يومي/فوري", callback_data="add_sched_start")],
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])

    await callback.message.edit_text(jobs_text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "add_sched_start")
async def add_schedule_prompt(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ رجوع", callback_data="menu_scheduler")]
    ])
    await callback.message.edit_text(
        "💡 **توجيهات الجدولة:**\n\n"
        "يمكنك إضافة المهام عبر لوحة الإدارة المتكاملة.\n"
        "المحرك الحالي يدعم الجدولة الزمنية الدقيقة وتخزينها بقاعدة البيانات.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()