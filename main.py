import os
from random import choice
from bs4 import BeautifulSoup  # для парсинга старниц
import requests                # для запросов к сайту, получения содержимого веб-страницы
from requests import get
import telebot

c = []
baza = {}
coins = []
token = "1665076762:AAHgbY056ymh0JiBKpdpt85ihkIW_iLq3JY"


def pars_info():
    url = 'https://coinmarketcap.com/'
    print(url)
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    coin_data = html_soup.find_all('tr')
    if coin_data != []:
        for i in range(10):
            coins.extend(coin_data)
    else:
        print('empty')

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


c = baza.keys()
a = ",".join(list(c))


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def welcome_start(message):
        bot.send_message(
            message.chat.id, 'Выполнил, Черноколпаков Илья\n'"Вот список доступных команд: список, обновить, поиск")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower() == "список":
            bot.send_message(
                message.chat.id, "Вот список монет, которые удалось спарсить: ")
            bot.send_message(message.chat.id, ", ".join(list(c)))
        if message.text.lower() == "обновить":
            pars_info()
            bot.send_message(message.chat.id, "Информация обновлена")
        if message.text.lower() == "поиск":
            mess = bot.send_message(message.chat.id, "Введите название")
            bot.register_next_step_handler(mess, POISK)
        if (message.text.lower() != "поиск" and message.text.lower() != "обновить" and message.text.lower() != "список"):bot.send_message(
            message.chat.id, 'Такой команды нет:( \n'"Вот список доступных команд: список, обновить, поиск")

    def POISK(message):
        key = message.text
        bot.send_message(message.chat.id, key)
        poisk = baza.get(key, "Такой валюты нет")
        bot.send_message(message.chat.id, ", ".join(list(poisk)))

    bot.polling()


if __name__ == "__main__":
    pars_info()

    telegram_bot(token)
