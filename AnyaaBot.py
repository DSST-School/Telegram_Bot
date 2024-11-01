import telebot
from datetime import datetime

# Вставьте ваш токен, полученный у @BotFather
TOKEN = 'ВАШ_ТОКЕН'
bot = telebot.TeleBot(TOKEN)

# Хранилище задач
tasks = {}

def send_message(user_id, text):
    bot.send_message(user_id, text)

def format_task_list(user_id):
    """Форматирует список задач для пользователя."""
    if user_id in tasks and tasks[user_id]:
        return "\n".join([f"{i + 1}. {task} на {time}" for i, (task, time) in enumerate(tasks[user_id])])
    return "У вас нет задач."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Привет! Я твой ежедневник. Используй команды:\n"
        "/add - добавить задачу\n"
        "/show - показать задачи\n"
        "/delete - удалить задачу\n"
        "/help - показать команды."
    )
    send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = (
        "/add - добавить задачу\n"
        "/show - показать задачи\n"
        "/delete - удалить задачу\n"
        "/help - показать команды."
    )
    send_message(message.chat.id, help_text)

@bot.message_handler(commands=['add'])
def add_task(message):
    msg = bot.send_message(message.chat.id, "Введите задачу и время в формате 'Задача, HH:MM'.")
    bot.register_next_step_handler(msg, save_task)

def save_task(message):
    user_id = message.chat.id
    try:
        task_text, task_time_str = map(str.strip, message.text.split(","))
        task_time = datetime.strptime(task_time_str, "%H:%M").time()

        tasks.setdefault(user_id, []).append((task_text, task_time))
        send_message(user_id, f"Задача '{task_text}' на {task_time} добавлена.")
    except ValueError:
        send_message(user_id, "Ошибка! Используйте формат 'Задача, HH:MM'.")

@bot.message_handler(commands=['show'])
def show_tasks(message):
    user_id = message.chat.id
    tasks_list = format_task_list(user_id)
    send_message(user_id, f"Ваши задачи на сегодня:\n{tasks_list}")

@bot.message_handler(commands=['delete'])
def delete_task(message):
    user_id = message.chat.id
    tasks_list = format_task_list(user_id)
    if tasks_list != "У вас нет задач.":
        msg = bot.send_message(user_id, f"Выберите номер задачи для удаления:\n{tasks_list}")
        bot.register_next_step_handler(msg, remove_task)
    else:
        send_message(user_id, tasks_list)

def remove_task(message):
    user_id = message.chat.id
    try:
        task_num = int(message.text) - 1
        task_text, task_time = tasks[user_id].pop(task_num)
        send_message(user_id, f"Задача '{task_text}' на {task_time} удалена.")
    except IndexError:
        send_message(user_id, "Ошибка! Номер задачи вне диапазона.")
    except ValueError:
        send_message(user_id, "Ошибка! Введите корректный номер задачи.")

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
