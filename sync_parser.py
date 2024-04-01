import requests
from bs4 import BeautifulSoup
import re
import socket
import time


# Проверка доступности сайта
def check_website(url: str) -> bool:
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


# Получение IP адреса хоста
def get_ip_address(host: str) -> str | None:
    try:
        ip_address = socket.gethostbyname(host)
        return ip_address
    except socket.gaierror:
        return None


# Получение телефона компании с главной страницы сайта
def get_phone_number(url: str) -> str | None:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        phone_number_element = soup.find('div', class_='phone-number')
        if phone_number_element:
            phone_number = phone_number_element.find('a').text.strip()
            # Убираем все символы, кроме цифр
            phone_number_digits = re.sub(r'\D', '', phone_number)
            # Приводим номер к нужному формату
            formatted_phone_number = re.sub(r'(\d)(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\2)\3-\4-\5', phone_number_digits)
            return formatted_phone_number
        else:
            return None
    except requests.RequestException:
        return None


# Проверка номера телефона на соответствие стандарту
def validate_phone_number(phone_number: str) -> re.Match[str]:
    # Убираем все символы, кроме цифр
    phone_number_digits = re.sub(r'\D', '', phone_number)
    # Паттерн для проверки соответствия стандарту
    pattern = r'^(\+\d{1,3})?(\d{1,6})(\d{3})(\d{2})(\d{2})$'
    return re.match(pattern, phone_number_digits)


def main():
    start_time = time.time()
    website_url = 'http://sstmk.ru'
    if check_website(website_url):
        print("Сайт доступен")
        ip_address = get_ip_address('sstmk.ru')
        if ip_address:
            print(f"IP адрес хоста sstmk.ru: {ip_address}")
            phone_number = get_phone_number(website_url)
            if phone_number:
                print("Найденный номер телефона компании:")
                print(phone_number)
                if validate_phone_number(phone_number):
                    print("Номер телефона соответствует стандарту")
                else:
                    print("Номер телефона не соответствует стандарту")
            else:
                print("На сайте не найден номер телефона компании")
        else:
            print("Не удалось получить IP адрес хоста")
    else:
        print("Сайт недоступен")

    end_time = time.time()
    print(f"Время выполнения: {end_time - start_time} секунд")


if __name__ == "__main__":
    main()
