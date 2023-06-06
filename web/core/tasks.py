import re
import time
from core.models import PersonTable, Person, CryptoObject
from celery import shared_task
from core.services import TableService, LeadVertexService
import requests
from bs4 import BeautifulSoup as bs
from django.shortcuts import redirect
from django.core.mail import send_mail
from core.telegram import send_notify


@shared_task
def save_table_task(loaded_table_id):
    loaded_table = PersonTable.objects.get(id=loaded_table_id)
    TableService.save_table(loaded_table)


@shared_task
def update_person_status_and_usage_by_phone_number():
    LeadVertexService.update_person_and_usage()


@shared_task
def check_price_crypto():
    while True:
        url = 'https://coinmarketcap.com/'
        resp = requests.get(url).text
        soup = bs(resp, 'lxml')
        tbody = soup.find('tbody')
        coins = tbody.find_all('tr')

        messege_telegram = "_______Оповещение_______\n"
        сrypto_name = []
        crypto_price = []
        counter = 0
        crypto_title = ['BTC', 'ETH', 'USDT', 'BNB', 'USDC', 'XRP', 'ADA', 'DOGE', 'SOL',
                        'MATIC']

        for coin in coins:
            href = coin.find(class_='cmc-link').get('href')
            main_href = url + href
            coin_url = requests.get(main_href)
            coin_soup = bs(coin_url.content, 'lxml')
            coinsybol = re.sub(r'(\<(/?[^>]+)>)', '', str(coin.find(class_='sc-4984dd93-0 iqdbQL coin-item-symbol')))
            coin_price = re.sub(r'(\<(/?[^>]+)>)', '', str(coin.find(class_='sc-cadad039-0 clgqXO'))).replace('$', '').replace(',', '')

            сrypto_name.append(coinsybol)
            crypto_price.append(coin_price)

            counter += 1
            if counter == 10:
                break

        for element in range(0, 10):
            try:
                if float(CryptoObject.objects.get(name=сrypto_name[element]).price_to_alert) >= float(crypto_price[element]):
                    messege_telegram = messege_telegram + f"\nНазвание монеты -- {CryptoObject.objects.get(name=сrypto_name[element]).name}\nЦена упала до {crypto_price[element]}\n"
                    CryptoObject.objects.get(name=сrypto_name[element]).delete()
            except:pass
        send_notify(messege_telegram)
        time.sleep(30)


@shared_task
def send_email_task(title, text):
    users_email = []
    for number in (1, Person.objects.count()):
        users_email.append(Person.objects.get(id=number).email)

    send_mail(subject=title,
              message=text,
              from_email='kolpackov.yarosl@gmail.com',
              recipient_list=users_email,
              fail_silently=False)
