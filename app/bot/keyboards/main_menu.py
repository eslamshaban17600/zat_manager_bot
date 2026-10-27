from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="📢 إدارة القنوات", callback_data="menu_channels"),
            InlineKeyboardButton(text="🗓️ جدولة المنشورات", callback_data="menu_scheduler")
        ],
        [
            InlineKeyboardButton(text="✍️ النشر الفوري", callback_data="menu_instant_post"),
            InlineKeyboardButton(text="📚 مكتبة المحتوى", callback_data="menu_content_lib")
        ],
        [
            InlineKeyboardButton(text="🌅 أذكار الصباح والمساء", callback_data="menu_adhkar"),
            InlineKeyboardButton(text="🌙 قيام الليل", callback_data="menu_night_prayer")
        ],
        [
            InlineKeyboardButton(text="📖 الختمات السماعية", callback_data="menu_quran"),
            InlineKeyboardButton(text="📝 الاختبارات", callback_data="menu_quizzes")
        ],
        [
            InlineKeyboardButton(text="📊 التقارير والإحصائيات", callback_data="menu_reports"),
            InlineKeyboardButton(text="⚙️ الإعدادات", callback_data="menu_settings")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 الرئيسية", callback_data="main_menu")]
    ])