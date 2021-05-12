import os
from random import choice
from bs4 import BeautifulSoup  # для парсинга старниц
import requests                # для запросов к сайту, получения содержимого веб-страницы
from requests import get
baza = {}
url = 'https://coinmarketcap.com/'
print(url)
response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')
coin_data = html_soup.find_all('tr')
coins = []
if coin_data != []:
    for i in range(10):
        coins.extend(coin_data)
else:
    print('empty')


def find_info(coins):

    for i in range(10):
        info = coins[int(i+1)]
        try:
            title = info.find(
                'p', {"class": "sc-1eb5slv-0 gGIpIK coin-item-symbol"}).text
        except:
            print('ошибка')

        try:
            price = info.find(
                'div', {"class": "price___3rj7O"}).text
        except:
            print('ошибка')

        try:
            MarketCap = info.find(
                'p', {"class": "sc-1eb5slv-0 kDEzev"}).text
        except:
            print('ошибка')

        baza[title] = "Стоимость валюты= "+price, "оборт= "+MarketCap

    return baza


while choice != 0:
    print("ВЫберите пункт: "
          "1 - спарсить информацию "
          "2 - вывести все названия "
          "3 - узнать информацию о конкретной валюте "
          )
    choice = input()
    if choice == "1":
        find_info(coins)
        input()
    if choice == "2":
        print(baza.keys())
        input()
    if choice == "3":
        os.system('cls')
        key = input(print("Ведите название валюты"))
        print(baza.get(key, "Такой валюты нет"))
        input()
