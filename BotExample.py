import telebot
import logging
import time
import configparser

# Загрузка токена из файла конфигурации
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config['TELEGRAM']['TOKEN']

# Инициализация бота и логгера
bot = telebot.TeleBot(TOKEN)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_message(message, text):
    """Отправка сообщения с обработкой ошибок и логированием."""
    try:
        bot.reply_to(message, text)
        logging.info(f"Сообщение отправлено пользователю {message.from_user.username}: {text}")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения пользователю {message.from_user.username}: {e}")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_message(message, "Привет! Я ваш бот. Как я могу помочь вам?\nВведите /help для списка команд.")

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
    send_message(message, help_text)

# Обработчик команды /info
@bot.message_handler(commands=['info'])
def send_info(message):
    send_message(message, "Я - бот, созданный для демонстрации возможностей Telegram API.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    send_message(message, f"Вы написали: {message.text}")

# Обработчик медиафайлов (например, фото)
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    send_message(message, "Спасибо за фото!")

# Дополнительные обработчики для различных типов сообщений
@bot.message_handler(content_types=['video', 'audio', 'document'])
def handle_media(message):
    send_message(message, "Спасибо за медиафайл!")

# Обработчик ошибок
def handle_error():
    while True:
        try:
            bot.polling()
        except Exception as e:
            logging.error(f"Ошибка при запуске бота: {e}")
            time.sleep(15)  # Перезапуск через 15 секунд

# Запускаем бота
if __name__ == '__main__':
    logging.info("Запуск бота...")
    handle_error()
