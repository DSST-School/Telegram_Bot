import telebot

# Вставьте свой токен, полученный от BotFather
TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш бот. Как я могу помочь вам?")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Доступные команды:\n/start - начать общение\n/help - помощь")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Вы написали: {message.text}")

# Запускаем бота
if __name__ == '__main__':
    bot.polling()
