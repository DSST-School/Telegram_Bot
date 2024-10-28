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

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.reply_to(message, "Привет! Я ваш бот. Как я могу помочь вам?\nВведите /help для списка команд.")
        logging.info(f"/start - Приветствие отправлено пользователю {message.from_user.username}")
    except Exception as e:
        logging.error(f"Ошибка при отправке приветствия: {e}")

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
    try:
        bot.reply_to(message, help_text)
        logging.info(f"/help - Справка отправлена пользователю {message.from_user.username}")
    except Exception as e:
        logging.error(f"Ошибка при отправке справки: {e}")

# Обработчик команды /info
@bot.message_handler(commands=['info'])
def send_info(message):
    try:
        bot.reply_to(message, "Я - бот, созданный для демонстрации возможностей Telegram API.")
        logging.info(f"/info - Информация отправлена пользователю {message.from_user.username}")
    except Exception as e:
        logging.error(f"Ошибка при отправке информации: {e}")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        bot.reply_to(message, f"Вы написали: {message.text}")
        logging.info(f"Ответ отправлен на сообщение пользователя {message.from_user.username}: {message.text}")
    except Exception as e:
        logging.error(f"Ошибка при ответе на текстовое сообщение: {e}")

# Обработчик медиафайлов (например, фото)
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.reply_to(message, "Спасибо за фото!")
        logging.info(f"Фото получено от пользователя {message.from_user.username}")
    except Exception as e:
        logging.error(f"Ошибка при обработке фото: {e}")

# Дополнительные обработчики для различных типов сообщений
@bot.message_handler(content_types=['video', 'audio', 'document'])
def handle_media(message):
    try:
        bot.reply_to(message, "Спасибо за медиафайл!")
        logging.info(f"Медиафайл получен от пользователя {message.from_user.username}")
    except Exception as e:
        logging.error(f"Ошибка при обработке медиафайла: {e}")

# Обработчик ошибок
def handle_error():
    try:
        bot.polling()
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
        time.sleep(15)  # Перезапуск через 15 секунд

# Запускаем бота с обработкой ошибок
if __name__ == '__main__':
    logging.info("Запуск бота...")
    while True:
        handle_error()
