# Импорт необходимых библиотек

from datetime import datetime
#import logging
import requests
from zoneinfo import ZoneInfo

from setup import BASE_URL


# Функция для создания сессии

def get_session(username: str, password: str) -> requests.Session | None:
    session = requests.Session()

    payload = {
        "username": username,
        "password": password
    }
    url = f"{BASE_URL}/login"

    try:
        response = session.post(url, json=payload)

        if response:
            answer = response.json()
            # Тут сделать логи и записать в них answer["msg"]

            if answer["success"]:
                return session
        else:
            # Тут сделать логи и записать в них response.status_code
            pass
    
    except Exception:
        # Тут сделать логи и записать в них Exception
        pass

    return None


# Функция для получения списка пользователей

def get_user_list(session: requests.Session) -> list[str]:
    result = []
    url = f"{BASE_URL}/panel/api/clients/list"


    try:
        response = session.get(url)

        if response:
            answer = response.json()

            for element in answer["obj"]:
                id = element["id"]
                email = element["email"]
                comment = element["comment"]
                if element["traffic"]["lastOnline"]:
                    last_online_int = datetime.fromtimestamp(element["traffic"]["lastOnline"] / 1000.0, tz=ZoneInfo("Europe/Moscow"))
                    last_online = last_online_int.strftime("%d.%m.%Y %H:%M:%S")
                else:
                    last_online = "Никогда"
                
                string = f"({id}) [{email}] -- '{comment}', последний раз в сети: {last_online}"
                result.append(string)
            
            return result
        else:
            # Тут сделать логи и записать в них response.status_code
            pass

    except Exception:
        # Тут сделать логи и записать в них Exception
        pass

    return None


# Функция для добавления нового пользователя

def add_user(session: requests.Session, comment: str) -> str:
    url = f"{BASE_URL}/api/clients/add"

    payload = {
        "client": {
            "email": "alice@example.com",
            "totalGB": 0,
            "expiryTime": 0,
            "tgId": 0,
            "limitIp": 1,
            "enable": True,
            "comment": comment

        },
        "inboundIds": [
            1,
            2,
            3
        ]
    }

    try:
        response = session.post(url, json=payload)

        if response:
            answer = response.json()

            if answer["success"]:
                return "Клиент добавлен"
            else:
                pass
        else:
            # Тут сделать логи и записать в них response.status_code
            pass

    except Exception:
        # Тут сделать логи и записать в них Exception
        pass

    return "Произошла ошибка, клиент не добавлен"
