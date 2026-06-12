# Импорт необходимых библиотек

import os
from dotenv import load_dotenv


# Получение всех нужных токенов лежащих в .env

load_dotenv()

API = os.getenv("API")
TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = int(os.getenv("TG_CHAT_ID"))

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


# Создание необходимой файловой структуры (логи)

try:
    os.mkdir("logs/")
except Exception:
    pass


# ДОБАВИТЬ: Настройка логирования