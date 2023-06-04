from core.models import PersonTable, Person
from celery import shared_task
from core.services import TableService, LeadVertexService
import requests
from bs4 import BeautifulSoup as bs
from django.shortcuts import redirect
from django.core.mail import send_mail


@shared_task
def save_table_task(loaded_table_id):
    loaded_table = PersonTable.objects.get(id=loaded_table_id)
    TableService.save_table(loaded_table)


@shared_task
def update_person_status_and_usage_by_phone_number():
    LeadVertexService.update_person_and_usage()


@shared_task
def check_price_crypto():
    return redirect('/')
    url = 'https://coinmarketcap.com/'
    resp = requests.get(url).text
    soup = bs(resp, 'lxml')
    tbody = soup.find('tbody')
    coins = tbody.find_all('tr')

    counter = 0
    for coin in coins:
        href = coin.find(class_='cmc-link').get('href')
        main_href = url + href
        coin_url = requests.get(main_href)
        coin_soup = bs(coin_url.content, 'lxml')
        coin_name = href.replace('/currencies/', "")[:-1]
        coinprice = coin.find(class_='sc-cadad039-0 clgqXO').text
        coinsybol = coin.find(class_='sc-4984dd93-0 iqdbQL coin-item-symbol').text
        counter += 1
        return redirect('/')
        if counter == 10:
            return redirect('/')
            break


@shared_task
def send_email_task(title, text):
    for number in (1, Person.objects.count()):

        send_mail(subject=title,
                    message=text,
                    from_email='kolpackov.yarosl@gmail.com',
                    recipient_list=[Person.objects.get(id=number).email],
                    fail_silently=False)

