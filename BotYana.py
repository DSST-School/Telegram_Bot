import telebot

# Замените 'YOUR_BOT_TOKEN' на ваш токен
API_TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Приветственное сообщение
WELCOME_MESSAGE = "Привет! Я Telegram-бот. Чем могу помочь?"
HELP_MESSAGE = "Я могу ответить на ваши сообщения. Просто напишите мне что-нибудь!"

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, WELCOME_MESSAGE)

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, HELP_MESSAGE)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Вы написали: {message.text}")

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
