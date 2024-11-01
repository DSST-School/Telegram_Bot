import telebot
from datetime import datetime
import json
import os

TOKEN = 'ВАШ_ТОКЕН_ТУТ'
bot = telebot.TeleBot(TOKEN)

# Путь к файлу для хранения данных
DATA_FILE = 'finances.json'

# Загрузка данных из файла
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Сохранение данных в файл
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Словарь для хранения данных о финансах
finances = load_data()

def send_message(chat_id, text):
    """Utility function to send a message."""
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['start'])
def start(message):
    send_message(
        message.chat.id,
        "Привет! Я финансовый бот. "
        "Я могу помочь вам вести учёт расходов и доходов. "
        "Отправьте /help для списка команд."
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    send_message(
        message.chat.id,
        "Команды:\n"
        "/income <сумма> - Добавить доход\n"
        "/expense <сумма> - Добавить расход\n"
        "/balance - Показать текущий баланс\n"
        "/history - Показать историю операций"
    )

def add_transaction(chat_id, transaction_type, amount):
    """Add a transaction to the finances dictionary."""
    finances.setdefault(str(chat_id), []).append((transaction_type, amount, datetime.now().isoformat()))
    save_data(finances)

@bot.message_handler(commands=['income'])
def add_income(message):
    chat_id = message.chat.id
    try:
        amount = float(message.text.split()[1])
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")
        add_transaction(chat_id, "Доход", amount)
        send_message(chat_id, f"Доход в размере {amount:.2f} добавлен.")
    except (IndexError, ValueError) as e:
        send_message(chat_id, f"Ошибка: {str(e)}. Пожалуйста, укажите корректную сумму дохода.")

@bot.message_handler(commands=['expense'])
def add_expense(message):
    chat_id = message.chat.id
    try:
        amount = float(message.text.split()[1])
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")
        add_transaction(chat_id, "Расход", -amount)
        send_message(chat_id, f"Расход в размере {amount:.2f} добавлен.")
    except (IndexError, ValueError) as e:
        send_message(chat_id, f"Ошибка: {str(e)}. Пожалуйста, укажите корректную сумму расхода.")

@bot.message_handler(commands=['balance'])
def check_balance(message):
    chat_id = message.chat.id
    balance = sum(item[1] for item in finances.get(str(chat_id), []))
    send_message(chat_id, f"Ваш текущий баланс: {balance:.2f}")

@bot.message_handler(commands=['history'])
def show_history(message):
    chat_id = message.chat.id
    transactions = finances.get(str(chat_id), [])
    
    if not transactions:
        send_message(chat_id, "История операций пуста.")
        return
    
    history = "\n".join([
        f"{datetime.fromisoformat(t[2]).strftime('%Y-%m-%d %H:%M')} - {t[0]}: {abs(t[1]):.2f}" for t in transactions
    ])
    send_message(chat_id, f"История операций:\n{history}")

if __name__ == "__main__":
    bot.polling(none_stop=True)
