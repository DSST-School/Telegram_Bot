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

# Определение команд и обработка сообщений
@bot.message_handler(commands=['start', 'help', 'info'])
def handle_commands(message):
    if message.text == '/start':
        response = "Привет! Я ваш бот. Как я могу помочь вам?\nВведите /help для списка команд."
    elif message.text == '/help':
        response = (
            "Доступные команды:\n"
            "/start - начать общение\n"
            "/help - помощь\n"
            "/info - информация о боте\n"
            "Просто напишите мне сообщение, и я повторю его!"
        )
    elif message.text == '/info':
        response = "Я - бот, созданный для демонстрации возможностей Telegram API."
    send_message(message, response)

# Обработчик текстовых и медиа сообщений
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'audio', 'document'])
def handle_all_messages(message):
    if message.content_type == 'text':
        response = f"Вы написали: {message.text}"
    elif message.content_type == 'photo':
        response = "Спасибо за фото!"
    else:
        response = "Спасибо за медиафайл!"
    send_message(message, response)

# Запуск бота с обработкой ошибок
def start_bot():
    while True:
        try:
            bot.polling()
        except Exception as e:
            logging.error(f"Ошибка при запуске бота: {e}")
            time.sleep(15)  # Перезапуск через 15 секунд

# Основной запуск
if __name__ == '__main__':
    logging.info("Запуск бота...")
    start_bot()
