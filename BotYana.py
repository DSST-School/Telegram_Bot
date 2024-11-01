import telebot

# Замените 'YOUR_BOT_TOKEN' на ваш токен
API_TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Сообщения
WELCOME_MESSAGE = "Привет! Я Telegram-бот. Чем могу помочь?"
HELP_MESSAGE = "Я могу ответить на ваши сообщения. Просто напишите мне что-нибудь!"

def send_message(message, text):
    """Отправляет текстовое сообщение."""
    bot.reply_to(message, text)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    send_message(message, WELCOME_MESSAGE)

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    send_message(message, HELP_MESSAGE)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    send_message(message, f"Вы написали: {message.text}")

# Запуск бота
if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка: {e}")

