import re
import time

import pycountry
import requests
from bs4 import BeautifulSoup
from flask import jsonify
from persiantools.jdatetime import JalaliDate, digits

from exchange.models.coin_commercial import CoinCommercial, coins_commercial_schema
from exchange.models.coin_single import CoinSingle, coins_single_schema
from exchange.models.currency import Currency, currencies_schema
from exchange.models.mappers.coin_mapper import mapToSingleEntity, mapToCommercialEntity
from exchange.models.mappers.currency_mapper import mapToEntity
from . import db

mouth_names = {
    "فروردین": 1,
    "اردیبهشت": 2,
    "خرداد": 3,
    "تیر": 4,
    "مرداد": 5,
    "شهریور": 6,
    "مهر": 7,
    "آبان": 8,
    "آذر": 9,
    "دی": 10,
    "بهمن": 11,
    "اسفند": 12
}


def fetch_currency():
    routes = [
        'currency',
        'currency-minor'
    ]

    classNames = [
        'table.data-table.market-table.market-section-right.active',
        'table.data-table.market-table.active'
    ]

    currency = []

    for route in routes:
        for className in classNames:
            currency += fetch_fields(route=route, className=className)

    return currency


def fetch_coin():
    dump_coin_single = fetch_fields(
        route='coin', className='table.data-table.market-table.market-section-right')
    dump_coin_commercial = fetch_fields(
        route='coin', className='table.data-table.market-table.mobile-half')

    return [
        dump_coin_single,
        dump_coin_commercial
    ]


def save_to_database():
    data_currency = fetch_currency()
    data_coin = fetch_coin()

    if data_currency and data_coin:
        db.session.query(Currency).delete()
        db.session.query(CoinSingle).delete()
        db.session.query(CoinCommercial).delete()

        for currency in data_currency:
            rate_currency = mapToEntity(currency)
            db.session.add(rate_currency)

        for coin in data_coin[0]:
            rate_coin_single = mapToSingleEntity(coin)
            db.session.add(rate_coin_single)

        for coin in data_coin[1]:
            rate_coin_commercial = mapToCommercialEntity(coin)
            db.session.add(rate_coin_commercial)

        db.session.commit()

        return jsonify(message="success", status=200,
                       currency=data_currency, coin_single=data_coin[0], coin_commercial=data_coin[1]), 200


def get_currencies(limit=None):
    currencies = Currency.query.limit(limit).all() if limit else Currency.query.all()
    data = currencies_schema.dump(currencies)

    return data


def get_coin_single(limit=None):
    coins = CoinSingle.query.limit(limit).all() if limit else CoinSingle.query.all()
    data = coins_single_schema.dump(coins)

    return data


def get_coin_commercial(limit=None):
    coins = CoinCommercial.query.limit(limit).all() if limit else CoinCommercial.query.all()
    data = coins_commercial_schema.dump(coins)

    return data


def fetch_fields(route, className):
    base_url = "https://www.tgju.org/"
    resp = requests.get(base_url+route)
    html = BeautifulSoup(resp.text, 'html.parser')
    data = []

    tables = html.select(className)
    if route == 'coin':
        tables = tables[:1]
        
    for table in tables:
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        for row in rows:
            field = row.findChildren(['th', 'td'], recursive=True)
            indicator = field[2].find('span').attrs['class']
            item = {
                "title": field[0].text,
                "prices": [{
                    "live": field[1].text,
                    "change": get_sign(indicator) + field[2].text,
                    "min": field[3].text,
                    "max": field[4].text
                }],
                "time": get_date(field[5].text)
            }
            if route != 'coin':
                alpha2 = str(field[0].find('span').attrs['class']
                             [1].replace('flag-', '')).upper()
                item.update({
                    "codes": [{
                        "alpha2": alpha2,
                        "alpha3": 'USD' if row['data-market-row'] == 'price_dollar_rl'
                            else row['data-market-row'].replace('price_', '').upper()
                            }],
                    "country": get_country(alpha2),
                })
            data.append(item)
    return data


def get_sign(indicator):
    if 'high' in indicator:
        return '+ '
    elif 'low' in indicator:
        return '- '
    return ''


def get_date(jalaliDate):
    date = ''

    try:
        t = time.strptime(digits.fa_to_en(jalaliDate), '%H:%M:%S')
        date = str('Today: ') + str(t.tm_hour) + ':' + \
            str(t.tm_min) + ':' + str(t.tm_sec)
    except ValueError:
        today = JalaliDate.today()
        check_mouth = (re.split(r'\s', jalaliDate))
        mouth_day = int(check_mouth[0])
        mouth_name = check_mouth[1]

        if str(mouth_name) in mouth_names:
            date = JalaliDate(today.year, int(
                mouth_names[mouth_name]), mouth_day).strftime("%m/%d")

    return date


def get_country(alpha2):
    country = pycountry.countries.get(alpha_2=alpha2)
    return country.name if country else alpha2
