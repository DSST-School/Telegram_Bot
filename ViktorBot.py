import telebot
from datetime import datetime

# Токен, полученный от BotFather
TOKEN = 'ВАШ_ТОКЕН_ТУТ'
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения данных о финансах
finances = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я финансовый бот. "
        "Я могу помочь вам вести учёт расходов и доходов. "
        "Отправьте /help для списка команд."
    )

# Команда /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "Команды:\n"
        "/income <сумма> - Добавить доход\n"
        "/expense <сумма> - Добавить расход\n"
        "/balance - Показать текущий баланс\n"
        "/history - Показать историю операций"
    )

# Команда для добавления дохода
@bot.message_handler(commands=['income'])
def add_income(message):
    chat_id = message.chat.id
    try:
        amount = float(message.text.split()[1])
        finances.setdefault(chat_id, []).append(("Доход", amount, datetime.now()))
        bot.send_message(chat_id, f"Доход в размере {amount:.2f} добавлен.")
    except (IndexError, ValueError):
        bot.send_message(chat_id, "Пожалуйста, укажите корректную сумму дохода после команды.")

# Команда для добавления расхода
@bot.message_handler(commands=['expense'])
def add_expense(message):
    chat_id = message.chat.id
    try:
        amount = float(message.text.split()[1])
        finances.setdefault(chat_id, []).append(("Расход", -amount, datetime.now()))
        bot.send_message(chat_id, f"Расход в размере {amount:.2f} добавлен.")
    except (IndexError, ValueError):
        bot.send_message(chat_id, "Пожалуйста, укажите корректную сумму расхода после команды.")

# Команда для проверки баланса
@bot.message_handler(commands=['balance'])
def check_balance(message):
    chat_id = message.chat.id
    balance = sum(item[1] for item in finances.get(chat_id, []))
    bot.send_message(chat_id, f"Ваш текущий баланс: {balance:.2f}")

# Команда для вывода истории операций
@bot.message_handler(commands=['history'])
def show_history(message):
    chat_id = message.chat.id
    transactions = finances.get(chat_id, [])
    
    if not transactions:
        bot.send_message(chat_id, "История операций пуста.")
        return
    
    history = "\n".join([
        f"{t[2].strftime('%Y-%m-%d %H:%M')} - {t[0]}: {t[1]:.2f}" for t in transactions
    ])
    bot.send_message(chat_id, f"История операций:\n{history}")

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
