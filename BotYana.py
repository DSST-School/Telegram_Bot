import telebot

# Замените 'YOUR_BOT_TOKEN' на ваш токен
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Telegram-бот. Чем могу помочь?")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Я могу ответить на ваши сообщения. Просто напишите мне что-нибудь!")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Вы написали: {message.text}")

# Запуск бота
bot.polling(none_stop=True)
