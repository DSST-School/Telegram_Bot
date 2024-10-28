import telebot
import logging

# Вставьте свой токен, полученный от BotFather
TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш бот. Как я могу помочь вам?\nВведите /help для списка команд.")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Доступные команды:\n"
        "/start - начать общение\n"
        "/help - помощь\n"
        "/info - информация о боте\n"
        "Просто напишите мне сообщение, и я повторю его!"
    )
    bot.reply_to(message, help_text)

# Обработчик команды /info
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "Я - бот, созданный для демонстрации возможностей Telegram API.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Вы написали: {message.text}")

# Обработчик медиафайлов
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "Спасибо за фото!")

# Обработчик ошибок
@bot.error_handler()
def handle_error(error):
    logging.error(f"Ошибка: {error}")

# Запускаем бота
if __name__ == '__main__':
    try:
        bot.polling()
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
