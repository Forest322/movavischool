from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import sqlite3
import logging

# Настройка логов
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация бота
TOKEN = "токен"
ADMIN_ID = 123456789
DB_NAME = "bot_database.db"

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            role TEXT NOT NULL,
            username TEXT
        )
    """)
    conn.commit()
    conn.close()

# Сохраняем пользователя в БД
def save_user(user_id, role, username=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (id, role, username) VALUES (?, ?, ?)", 
                  (user_id, role, username))
    conn.commit()
    conn.close()

# Получаем роль пользователя
def get_user_role(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# ===== ОСНОВНЫЕ ФУНКЦИИ БОТА =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Я преподаватель", callback_data='teacher')],
        [InlineKeyboardButton("Я куратор", callback_data='curator')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text('Привет! Выберите свою роль:', reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(
            text='Привет! Выберите свою роль:',
            reply_markup=reply_markup
        )

# ===== ФУНКЦИИ ПРЕПОДАВАТЕЛЯ =====

async def teacher_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    save_user(query.from_user.id, "teacher", query.from_user.username)
    
    keyboard = [
        [InlineKeyboardButton("О компании", callback_data='teacher_about')],
        [InlineKeyboardButton("Структура", callback_data='teacher_structure')],
        [InlineKeyboardButton("Карта курсов", callback_data='teacher_courses')],
        [InlineKeyboardButton("Партнеры", callback_data='teacher_partners')],
        [InlineKeyboardButton("Мотивация", callback_data='teacher_motivation')],
        [InlineKeyboardButton("Метод работы", callback_data='teacher_method')],
        [InlineKeyboardButton("Назад в начало", callback_data='back_to_start')]
    ]
    await query.edit_message_text(
        text="Меню преподавателя:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def teacher_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    text = "📚 О компании:\n\nМы - образовательная платформа..."
    keyboard = [
        [InlineKeyboardButton("Подробнее на сайте", url="https://example.com/about")],
        [InlineKeyboardButton("Назад", callback_data='back_to_teacher')]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def teacher_structure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    text = "🏢 Структура компании:\n\n1. Учебный отдел\n2. Методический отдел..."
    keyboard = [
        [InlineKeyboardButton("Подробнее", url="https://example.com/structure")],
        [InlineKeyboardButton("Назад", callback_data='back_to_teacher')]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def teacher_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Основные курсы", url="https://example.com/main_courses")],
        [InlineKeyboardButton("Летняя школа", url="https://example.com/summer_school")],
        [InlineKeyboardButton("Назад", callback_data='back_to_teacher')]
    ]
    await query.edit_message_text(
        text="Выберите тип курсов:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def teacher_partners(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("РОСТ", callback_data='teacher_rost')],
        [InlineKeyboardButton("ПРОСКУЛ", callback_data='teacher_proskul')],
        [InlineKeyboardButton("10-я гимназия", callback_data='teacher_gym10')],
        [InlineKeyboardButton("Назад", callback_data='back_to_teacher')]
    ]
    await query.edit_message_text(
        text="Наши партнеры:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def teacher_rost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Олимпиада", url="https://example.com/rost/olympiad")],
        [InlineKeyboardButton("Курсы", url="https://example.com/rost/courses")],
        [InlineKeyboardButton("Назад к партнёрам", callback_data='teacher_partners')]
    ]
    await query.edit_message_text(
        text="РОСТ - доступные разделы:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def teacher_proskul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Курсы", url="https://example.com/proskul/courses")],
        [InlineKeyboardButton("Назад к партнёрам", callback_data='teacher_partners')]
    ]
    await query.edit_message_text(
        text="ПРОСКУЛ - доступные разделы:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def teacher_gym10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Курсы", url="https://example.com/gym10/courses")],
        [InlineKeyboardButton("Назад к партнёрам", callback_data='teacher_partners')]
    ]
    await query.edit_message_text(
        text="10-я гимназия - доступные разделы:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def teacher_motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Обратная связь", url="https://example.com/motivation/feedback")],
        [InlineKeyboardButton("Мовави Boost", url="https://example.com/motivation/movavi")],
        [InlineKeyboardButton("Назад", callback_data='back_to_teacher')]
    ]
    await query.edit_message_text(
        text="Мотивационная программа:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def teacher_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(
        text="Наш метод работы:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Описание метода", url="https://example.com/method")],
            [InlineKeyboardButton("Назад", callback_data='back_to_teacher')]
        ])
    )

# ===== ФУНКЦИИ КУРАТОРА =====

async def curator_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    save_user(query.from_user.id, "curator", query.from_user.username)
    
    keyboard = [
        [InlineKeyboardButton("О компании", callback_data='curator_about')],
        [InlineKeyboardButton("Инструкция и регламент", callback_data='curator_instructions')],
        [InlineKeyboardButton("Карта курсов", callback_data='curator_courses')],
        [InlineKeyboardButton("Структура", callback_data='curator_structure')],
        [InlineKeyboardButton("Партнеры", callback_data='curator_partners')],
        [InlineKeyboardButton("Мотивация", callback_data='curator_motivation')],
        [InlineKeyboardButton("Полезные телефоны", callback_data='curator_phones')],
        [InlineKeyboardButton("Назад в начало", callback_data='back_to_start')]
    ]
    await query.edit_message_text(
        text="Меню куратора:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def curator_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(
        text="Информация о компании для кураторов:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Назад", callback_data='back_to_curator')]
        ])
    )

async def curator_instructions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Документооборот", url="https://example.com/guide/document-flow")],
        [InlineKeyboardButton("Касса", url="https://example.com/guide/cash-register")],
        [InlineKeyboardButton("Назад", callback_data='back_to_curator')]
    ]
    await query.edit_message_text(
        text="📚 Инструкции и регламенты:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def curator_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Летняя школа", url="https://example.com/courses/summer")],
        [InlineKeyboardButton("Основные курсы", url="https://example.com/courses/main")],
        [InlineKeyboardButton("Назад", callback_data='back_to_curator')]
    ]
    await query.edit_message_text(
        text="Карта курсов для кураторов:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def curator_structure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(
        text="Структура компании:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Подробнее", url="https://example.com/structure")],
            [InlineKeyboardButton("Назад", callback_data='back_to_curator')]
        ])
    )

async def curator_partners(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("РОСТ", callback_data='curator_rost')],
        [InlineKeyboardButton("ПРОСКУЛ", callback_data='curator_proskul')],
        [InlineKeyboardButton("Назад", callback_data='back_to_curator')]
    ]
    await query.edit_message_text(
        text="Партнеры компании:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def curator_rost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Олимпиада", url="https://example.com/rost/olympiad")],
        [InlineKeyboardButton("Назад к партнёрам", callback_data='curator_partners')]
    ]
    await query.edit_message_text(
        text="РОСТ - доступные разделы:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def curator_proskul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Курсы", url="https://example.com/proskul/courses")],
        [InlineKeyboardButton("Назад к партнёрам", callback_data='curator_partners')]
    ]
    await query.edit_message_text(
        text="ПРОСКУЛ - доступные разделы:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def curator_motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Обратная связь", url="https://example.com/motivation/feedback")],
        [InlineKeyboardButton("Назад", callback_data='back_to_curator')]
    ]
    await query.edit_message_text(
        text="Мотивационная программа:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def curator_phones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(
        text="Полезные телефоны:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Список телефонов", url="https://example.com/phones")],
            [InlineKeyboardButton("Назад", callback_data='back_to_curator')]
        ])
    )

# ===== ОБРАБОТКА КНОПОК =====

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    handlers = {
        'teacher': teacher_menu,
        'curator': curator_menu,
        'back_to_teacher': teacher_menu,
        'back_to_curator': curator_menu,
        'back_to_start': start,
        'teacher_about': teacher_about,
        'teacher_structure': teacher_structure,
        'teacher_courses': teacher_courses,
        'teacher_partners': teacher_partners,
        'teacher_motivation': teacher_motivation,
        'teacher_method': teacher_method,
        'teacher_rost': teacher_rost,
        'teacher_proskul': teacher_proskul,
        'teacher_gym10': teacher_gym10,
        'curator_about': curator_about,
        'curator_instructions': curator_instructions,
        'curator_courses': curator_courses,
        'curator_structure': curator_structure,
        'curator_partners': curator_partners,
        'curator_motivation': curator_motivation,
        'curator_phones': curator_phones,
        'curator_rost': curator_rost,
        'curator_proskul': curator_proskul
    }
    
    if query.data in handlers:
        await handlers[query.data](update, context)

# ===== ЗАПУСК БОТА =====

def main():
    init_db()  # Инициализация базы данных
    
    app = Application.builder().token(TOKEN).build()
    
    # Обработчики команд
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    logger.info("Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()