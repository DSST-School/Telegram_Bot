import telebot
from datetime import datetime

# Вставьте ваш токен, полученный у @BotFather
TOKEN = 'ВАШ_ТОКЕН'
bot = telebot.TeleBot(TOKEN)

# Хранилище задач, в реальном приложении лучше использовать базу данных
tasks = {}

# Команда старт для приветствия
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой ежедневник. Используй команды:\n/add - добавить задачу\n/show - показать задачи\n/delete - удалить задачу\n/help - показать команды.")

# Команда help для вывода всех доступных команд
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, "/add - добавить задачу\n/show - показать задачи\n/delete - удалить задачу\n/help - показать команды.")

# Команда для добавления задачи
@bot.message_handler(commands=['add'])
def add_task(message):
    msg = bot.send_message(message.chat.id, "Введите задачу и время в формате 'Задача, HH:MM'.")
    bot.register_next_step_handler(msg, save_task)

def save_task(message):
    try:
        task_text, task_time = message.text.split(", ")
        task_time = datetime.strptime(task_time, "%H:%M").time()
        user_id = message.chat.id

        if user_id not in tasks:
            tasks[user_id] = []
        
        tasks[user_id].append((task_text, task_time))
        bot.send_message(user_id, f"Задача '{task_text}' на {task_time} добавлена.")
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Используйте формат 'Задача, HH:MM'.")

# Команда для показа всех задач
@bot.message_handler(commands=['show'])
def show_tasks(message):
    user_id = message.chat.id
    if user_id in tasks and tasks[user_id]:
        tasks_list = "\n".join([f"{task} на {time}" for task, time in tasks[user_id]])
        bot.send_message(user_id, f"Ваши задачи на сегодня:\n{tasks_list}")
    else:
        bot.send_message(user_id, "У вас нет задач.")

# Команда для удаления задачи
@bot.message_handler(commands=['delete'])
def delete_task(message):
    user_id = message.chat.id
    if user_id in tasks and tasks[user_id]:
        tasks_list = "\n".join([f"{i + 1}. {task} на {time}" for i, (task, time) in enumerate(tasks[user_id])])
        msg = bot.send_message(user_id, f"Выберите номер задачи для удаления:\n{tasks_list}")
        bot.register_next_step_handler(msg, remove_task)
    else:
        bot.send_message(user_id, "У вас нет задач для удаления.")

def remove_task(message):
    user_id = message.chat.id
    try:
        task_num = int(message.text) - 1
        task_text, task_time = tasks[user_id].pop(task_num)
        bot.send_message(user_id, f"Задача '{task_text}' на {task_time} удалена.")
    except (IndexError, ValueError):
        bot.send_message(user_id, "Ошибка! Введите корректный номер задачи.")

# Запуск бота
bot.polling(none_stop=True)
