# Импорт необходимых библиотек

from datetime import datetime
import inspect
#import logging
import random
import requests
from zoneinfo import ZoneInfo

from setup import BASE_URL, LIMIT_IP, TOTAL_GB, INBOUNDS_IDS


# Функция для создания сессии

def get_session(username: str, password: str) -> requests.Session | None:
    session = requests.Session()

    payload = {
        "username": username,
        "password": password
    }
    url = f"{BASE_URL}/login"

    try:
        response = session.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            answer = response.json()
            success = answer.get("success", False)
            # msg = answer.get("msg", "Нет ответа от сервера")
            # Тут сделать логи и записать в них answer["msg"]

            if success:
                return session
        else:
            # Тут сделать логи и записать в них response.status_code
            pass
    
    except Exception:
        # Тут сделать логи и записать в них Exception
        pass

    return None


# Функция для получения списка пользователей

def get_user_list(session: requests.Session) -> list[str] | None:
    result = []
    url = f"{BASE_URL}/panel/api/clients/list"


    try:
        response = session.get(url, timeout=10)

        if response.status_code == 200:
            answer = response.json()
            elements = answer.get("obj")
            if not elements:
                return []

            for element in elements:
                client_id = element.get("id", "id Неизвестен")
                email = element.get("email", "email Неизвестен")
                comment = element.get("comment", "comment Неизвестен")

                traffic = element.get("traffic", {})
                lastOnline = traffic.get("lastOnline") if traffic else None
                if lastOnline:
                    last_online_int = datetime.fromtimestamp(lastOnline / 1000.0, tz=ZoneInfo("Europe/Moscow"))
                    last_online = last_online_int.strftime("%d.%m.%Y %H:%M:%S")
                else:
                    last_online = "Никогда"
                
                string = f"({client_id}) [{email}] -- '{comment}', последний раз в сети: {last_online}"
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
    # Функция, генерирующая email
    def create_email() -> str:
        prefix = "user"

        let1 = chr(random.randint(97, 122))
        ch1 = random.randint(0, 9)
        let2 = chr(random.randint(97, 122))
        ch2 = random.randint(0, 9)
        random_id = f"{let1}{ch1}{let2}{ch2}"
        
        email = f"{prefix}_{random_id}"
        return email
        

    url = f"{BASE_URL}/api/clients/add"

    payload = {
        "client": {
            "email": create_email(),
            "totalGB": TOTAL_GB,
            "expiryTime": 0,
            "tgId": 0,
            "limitIp": LIMIT_IP,
            "enable": True,
            "comment": comment

        },
        "inboundIds": INBOUNDS_IDS
    }

    try:
        response = session.post(url, json=payload)

        if response:
            answer = response.json()
            success = answer.get("success", False)
            # msg = answer.get("msg", "Нет ответа от сервера")
            # Написать msg в логи

            if success:
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


# Функция для удаления пользователя по его email

def delete_user(session: requests.Session, email: str) -> str:
    # Функция для проверки существования email
    def check(session: requests.Session, email: str) -> bool:
        url = f"{BASE_URL}/panel/api/clients/list"

        try:
            response = session.get(url, timeout=10)

            if response.status_code == 200:
                answer = response.json()
                elements = answer.get("obj", [])

                for element in elements:
                    if email == element.get("email", False) and email:
                        return True
            else:
                # Тут сделать логи и записать в них response.status_code
                pass

        except Exception:
            # Тут сделать логи и записать в них Exception
            pass

        return False
    
    if check(session, email):
        url = f"{BASE_URL}/panel/api/clients/del/{email}?keepTraffic=1"

        try:
            response = session.post(url, timeout=10)

            if response.status_code == 200:
                answer = response.json()
                success = answer.get("success", False)
                # msg = answer.get("msg", "Нет ответа от сервера")
                # Написать msg в логи

                if success:
                    return f"Клиент '{email}'удален"                
            else:
                # Тут сделать логи и записать в них response.status_code
                pass

        except Exception:
            # Тут сделать логи и записать в них Exception
            return "Произошла ошибка, пользователь не был удален"
    
    return f"Данного email '{email}' не существует!"


# Функция для просмотра состояния сервера

def server_status(session: requests.Session) -> str:
    # Функция для перевода бит в гигабайты
    def byte_to_gb(x: int) -> str:
        try:
            result = x / (1024**3)
            return f"{result:.2f}"
        except Exception:
            return "Произошла ошибка"

    url = f"{BASE_URL}/api/server/status"

    try:
        response = session.get(url, timeout=10)
        
        if response:
            answer = response.json()
            success = answer.get("success", False)
            # msg = answer.get("msg", "Нет ответа от сервера")
            # Написать msg в логи

            if success:
                data = answer["obj"]

                ip = data.get("publicIP", {}).get("ipv4", "IP не найден")

                cpu = f"{data.get('cpu', 0.00):.1f}"
                cpu_cores = f"{data.get('cpuCores', 0)}"

                mem = data.get("mem", {})
                current_mem = byte_to_gb(mem.get("current", 0))
                total_mem = byte_to_gb(mem.get("total", 0))

                swap = data.get("swap", {})
                current_swap = byte_to_gb(swap.get("current", 0))
                total_swap = byte_to_gb(swap.get("total", 0))

                disk = data.get("disk", {})
                current_disk = byte_to_gb(disk.get("current", 0))
                total_disk = byte_to_gb(disk.get("total", 0))

                net_traffic = data.get("netTraffic", {})
                total_send  = byte_to_gb(net_traffic.get("sent", 0))
                total_get = byte_to_gb(net_traffic.get("recv", 0))

                panel_version = data.get("panelVersion", "0.00.00")

                xray = data.get("xray", {})
                xray_status = xray.get("state", "---")
                xray_version = xray.get("version", "0.00.00")

                result = f"""
                    #================================================#
                    IP:             {ip}
                    #================================================#
                    CPU:            {cpu}% ({cpu_cores} Core)
                    MEMORY:         {current_mem}/{total_mem} GB
                    SWAP:           {current_swap}/{total_swap} GB
                    DISK:           {current_disk}/{total_disk} GB
                    #================================================#
                    TOTAL SEND:     {total_send} GB
                    TOTAL GET:      {total_get} GB
                    #================================================#
                    PANEL VERSION:  {panel_version}
                    #================================================#
                    XRAY STATUS:    {xray_status}
                    XRAY VERSION:   {xray_version}
                    #================================================#
                """

                return inspect.cleandoc(result)
            else:
                pass
        else:
            # Тут сделать логи и записать в них response.status_code
            pass


    except Exception:
        # Тут сделать логи и записать в них Exception
        pass

    return "Произошла ошибка, невозможно узнать состояние сервера"


# Функция для обновления Web-панели

def update_panel(session: requests.Session) -> str:
    url = f"{BASE_URL}/api/server/updatePanel"

    try:
        response = session.post(url, timeout=10)

        if response.status_code == 200:
            answer = response.json()
            success = answer.get("success", False)
            # msg = answer.get("msg", "Нет ответа от сервера")
            # Написать msg в логи

            if success:
                return "Панель успешно обновлена!"
        else:
            # Тут сделать логи и записать в них response.status_code
            pass

    except Exception:
        # Тут сделать логи и записать в них Exception
        pass

    return "Произошла ошибка, панель не была обновлена"


# Функия для обновления xray

def restart_xray_service(session: requests.Session) -> str:
    url = f"{BASE_URL}/panel/api/server/restartXrayService"

    try:
        response = session.post(url, timeout=10)

        if response.status_code == 200:
            answer = response.json()
            success = answer.get("success", False)
            # msg = answer.get("msg", "Нет ответа от сервера")
            # Написать msg в логи

            if success:
                return "xray успешно перезапущен!"
        else:
            # Тут сделать логи и записать в них response.status_code
            pass

    except Exception:
        # Тут сделать логи и записать в них Exception
        pass
    
    return "Произошла ошибка, xray не был перезапущен"


# Функция для обновления Geofiles

def update_geofile(session: requests.Session) -> str:
    url = f"{BASE_URL}/panel/api/server/updateGeofile"

    try:
        response = session.post(url, timeout=30)

        if response.status_code == 200:
            answer = response.json()
            success = answer.get("success", False)
            # msg = answer.get("msg", "Нет ответа от сервера")
            # Написать msg в логи

            if success:
                return "Geofile успешно обновлен"
        else:
            # Тут сделать логи и записать в них response.status_code
            pass

    except Exception:
        # Тут сделать логи и записать в них Exception
        pass

    return "Произошла ошибка, не получилось обновить geofile"
