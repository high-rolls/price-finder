from decimal import Decimal, getcontext
from django.http import HttpRequest
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def index(request: HttpRequest):
    getcontext().prec = 2
    query = request.GET.get('q', None)
    if query is None:
        return render(request, 'price_finder/index.html', { 'products': None })

    response = requests.get(f'https://lista.mercadolivre.com.br/{query}')
    soup = BeautifulSoup(response.text, 'lxml')
    cards = soup('div', class_='poly-card__content')
    products = []
    for card in cards:
        title = card.find('a', class_='poly-component__title')
        title_text = ''
        if title is not None:
            title_text = title.get_text()
        
        price_text = ''
        price_fraction = card.find('span', class_='andes-money-amount__fraction')
        if price_fraction is not None:
            price_text = price_fraction.get_text().replace('.', '')
        
        price_cents = card.find('span', class_='andes-money-amount__cents')
        if price_cents is not None:
            price_text = price_text + '.' + price_cents.get_text()

        price = Decimal(price_text)
        products.append({ 'title': title_text, 'price': price })
    
    context = {
        'products': products
    }
    return render(request, 'price_finder/index.html', context)