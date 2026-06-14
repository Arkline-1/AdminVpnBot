# Импорт необходимых библиотек

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import logging
import os
import sys


# Получение всех нужных токенов лежащих в .env

load_dotenv()

try:
    API = os.getenv("API")
    TG_TOKEN = os.getenv("TG_TOKEN")
    TG_CHAT_ID = int(os.getenv("TG_CHAT_ID"))

    BASE_URL = os.getenv("BASE_URL")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")

    LIMIT_IP = int(os.getenv("LIMIT_IP"))
    TOTAL_GB = int(os.getenv("TOTAL_GB"))
    INBOUNDS_IDS = os.getenv("INBOUNDS_IDS").split(",")
except Exception as e:
    print(f"Ошибка при инициализации переменных: {e}")
    sys.exit()


# Создание необходимой файловой структуры (логи)

os.makedirs("logs/", exist_ok=True)


# Заготовка для функции для настройки логирования

def init_logging():
    logging.basicConfig(
        level = logging.INFO,                                                 # Будет логироваться все начиная с уровня INFO
        format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s",         # Формат
        datefmt = "%Y-%m-%d %H:%M:%S",                                        # Формат %(asctime)s
        handlers = [
            logging.StreamHandler(sys.stdout), 
            logging.FileHandler("logs/programm.log", encoding="utf-8") 
        ]                                                                     # Все места куда выводятся логи: консоль и файл programm.log
    )


# Инициализация телеграм бота
bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


# Вызов логирования (чтобы сразу работал при импорте)
init_logging()
logger = logging.getLogger(__name__)
logger.info("Конфигурация и логирование успешно инициализированны")
