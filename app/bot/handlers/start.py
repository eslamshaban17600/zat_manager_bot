from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.bot.keyboards.main_menu import get_main_menu_keyboard, get_back_to_main_keyboard

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    welcome_text = (
        "مرحباً بك في نظام **«ذآتـ 𓂆»** لإدارة القنوات الإسلامية.\n\n"
        "النظام مصمم خصيصاً لإدارة المحتوى، الجدولة المتقدمة، الأذكار، الختمات، والاختبارات بذكاء واحترافية عالية.\n\n"
        "اختر أحد الأقسام التالية من لوحة التحكم أدناه:"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "main_menu")
async def callback_main_menu(callback: CallbackQuery):
    welcome_text = "أهلاً بك مجدداً في لوحة التحكم الرئيسية لـ **«ذآتـ 𓂆»**:"
    await callback.message.edit_text(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data.startswith("menu_"))
async def handle_submenus(callback: CallbackQuery):
    section = callback.data.replace("menu_", "")
    titles = {
        "channels": "📢 قسم إدارة القنوات:\nيمكنك هنا إضافة القنوات والتحقق من صلاحيات البوت.",
        "scheduler": "🗓️ نظام جدولة المنشورات:\nإدارة المهام اليومية والأسبوعية والمؤقتة.",
        "instant_post": "✍️ محرر النشر الفوري:\nأرسل منشوراتك أو ألبومات الصور مباشرة.",
        "content_lib": "📚 مكتبة المحتوى الإسلامي:\nتخزين واسترجاع المنشورات والفوائد.",
        "adhkar": "🌅 أذكار الصباح والمساء:\nإدارة وجدولة الأذكار اليومية.",
        "night_prayer": "🌙 برنامج قيام الليل:\nضبط التذكيرات والرسائل الإيمانية.",
        "quran": "📖 الختمات السماعية:\nإدارة القراء والتلاوات وخطط الختم.",
        "quizzes": "📝 نظام الاختبارات والمسابقات:\nتوليد وإدارة الأسئلة.",
        "reports": "📊 التقارير والإحصائيات:\nعرض السجلات والنشاطات الناجحة والفاشلة.",
        "settings": "⚙️ الإعدادات العامة:\nالنسخ الاحتياطي وإعدادات النظام."
    }
    text = titles.get(section, "قسم قيد التطوير أو غير معروف.")
    await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
    await callback.answer()