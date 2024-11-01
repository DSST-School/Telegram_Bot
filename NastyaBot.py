import telebot
import requests
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Замените на токен вашего телеграм-бота и API-ключ OpenWeatherMap
TELEGRAM_TOKEN = 'ВАШ_ТЕЛЕГРАМ_ТОКЕН'
WEATHER_API_KEY = 'ВАШ_API_КЛЮЧ'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Функция для получения погоды
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()

        city_name = data['name']
        country = data['sys']['country']
        temperature = data['main']['temp']
        description = data['weather'][0]['description']

        return (f"Погода в {city_name}, {country}:\n"
                f"Температура: {temperature}°C\n"
                f"Описание: {description.capitalize()}")
    
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return "Не удалось получить погоду для этого города. Проверьте правильность названия и наличие подключения к интернету."
    except KeyError:
        logging.error("Некорректные данные от API")
        return "Не удалось найти информацию о погоде. Проверьте название города."
    except Exception as err:
        logging.error(f"Произошла неожиданная ошибка: {err}")
        return "Произошла ошибка при получении данных."

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Введите название города, чтобы узнать текущую погоду.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def send_weather(message):
    city = message.text.strip()
    if city:
        weather_info = get_weather(city)
        bot.reply_to(message, weather_info)
    else:
        bot.reply_to(message, "Пожалуйста, введите название города.")

# Запуск бота
if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)  # добавлено для непрерывной работы
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
