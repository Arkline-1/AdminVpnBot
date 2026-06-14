# Импорт необходимых библиотек

from dotenv import load_dotenv
# import logging
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
    pass
