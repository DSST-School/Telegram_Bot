import telebot
from telebot import types
import random
import logging

# Замените 'YOUR_TOKEN' на токен вашего бота
TOKEN = 'YOUR_TOKEN'
bot = telebot.TeleBot(TOKEN)

# Установка логирования
logging.basicConfig(level=logging.INFO)

# Словарь упражнений для различных групп мышц
EXERCISES = {
    "грудь": ["Жим лёжа", "Отжимания на брусьях", "Разводка гантелей"],
    "спина": ["Тяга верхнего блока", "Тяга гантели в наклоне", "Подтягивания"],
    "ноги": ["Приседания", "Выпады", "Жим ногами"],
    "руки": ["Сгибания на бицепс", "Французский жим", "Отжимания"],
    "плечи": ["Жим гантелей сидя", "Махи гантелями в стороны", "Армейский жим"]
}

# Стартовая команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Отправляет приветственное сообщение."""
    bot.reply_to(message, "Привет! Я фитнес-бот. Выберите группу мышц, для которой хотите получить упражнение.")

# Обработка команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    """Отправляет сообщение с помощью по командам."""
    help_text = (
        "Используйте команды:\n"
        "/start - начать\n"
        "/help - помощь\n"
        "/exercises - выбрать упражнение по группе мышц"
    )
    bot.reply_to(message, help_text)

# Команда /exercises для выбора группы мышц
@bot.message_handler(commands=['exercises'])
def send_exercise_options(message):
    """Отправляет клавиатуру с группами мышц."""
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    buttons = [types.KeyboardButton(muscle) for muscle in EXERCISES.keys()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Выберите группу мышц:", reply_markup=markup)

def get_random_exercise(muscle_group):
    """Возвращает случайное упражнение для данной группы мышц."""
    return random.choice(EXERCISES[muscle_group])

# Ответ на выбор группы мышц
@bot.message_handler(func=lambda message: message.text in EXERCISES)
def send_exercise(message):
    """Отправляет случайное упражнение для выбранной группы мышц."""
    muscle_group = message.text
    exercise = get_random_exercise(muscle_group)
    bot.send_message(message.chat.id, f"Упражнение для {muscle_group}: {exercise}")

# Обработка любого другого сообщения
@bot.message_handler(func=lambda message: True)
def handle_unrecognized_message(message):
    """Обрабатывает сообщения, которые не соответствуют командам."""
    bot.reply_to(message, "Используйте команду /exercises, чтобы выбрать группу мышц.")

# Запуск бота
if __name__ == '__main__':
    logging.info("Бот запущен.")
    bot.polling(none_stop=True)
