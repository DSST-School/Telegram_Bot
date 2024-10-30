import telebot
import requests

# Замените на токен вашего телеграм-бота и API-ключ OpenWeatherMap
TELEGRAM_TOKEN = 'ВАШ_ТЕЛЕГРАМ_ТОКЕН'
WEATHER_API_KEY = 'ВАШ_API_КЛЮЧ'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Функция для получения погоды
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data['name']
        country = data['sys']['country']
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        return f"Погода в {city}, {country}:\nТемпература: {temperature}°C\nОписание: {description.capitalize()}"
    else:
        return "Не удалось получить погоду для этого города. Проверьте правильность названия."

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Введите название города, чтобы узнать текущую погоду.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def send_weather(message):
    city = message.text
    weather_info = get_weather(city)
    bot.reply_to(message, weather_info)

# Запуск бота
bot.polling()
