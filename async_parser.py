import asyncio
import re
import time
import aiohttp
import socket
from bs4 import BeautifulSoup


# Проверка доступности сайта
async def check_website(url: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.status == 200
    except aiohttp.ClientError:
        return False


# Получение IP адреса хоста
async def get_ip_address(host: str) -> str | None:
    try:
        ip_address = await asyncio.get_event_loop().getaddrinfo(host, None)
        return ip_address[0][4][0]
    except socket.gaierror:
        return None


# Получение телефона компании с главной страницы сайта
async def get_phone_number(url: str) -> str | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                phone_number_element = soup.find('div', class_='phone-number')
                if phone_number_element:
                    phone_number = phone_number_element.find('a').text.strip()
                    # Убираем все символы, кроме цифр
                    phone_number_digits = re.sub(r'\D', '', phone_number)
                    # Приводим номер к нужному формату
                    formatted_phone_number = re.sub(r'(\d)(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\2)\3-\4-\5',
                                                    phone_number_digits)
                    return formatted_phone_number
                else:
                    return None
    except aiohttp.ClientError:
        return None


# Проверка номера телефона на соответствие стандарту
def validate_phone_number(phone_number: str) -> re.Match[str]:
    # Убираем все символы, кроме цифр
    phone_number_digits = re.sub(r'\D', '', phone_number)
    # Паттерн для проверки соответствия стандарту
    pattern = r'^(\+\d{1,3})?(\d{1,6})(\d{3})(\d{2})(\d{2})$'
    return re.match(pattern, phone_number_digits)


async def main():
    start_time = time.time()
    website_url = 'http://sstmk.ru'
    if await check_website(website_url):
        print("Сайт доступен")
        ip_address = await get_ip_address('sstmk.ru')
        if ip_address:
            print(f"IP адрес хоста sstmk.ru: {ip_address}")
            phone_number = await get_phone_number(website_url)
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
    asyncio.run(main())
