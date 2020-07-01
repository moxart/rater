import re
import time

import pycountry
import requests
from bs4 import BeautifulSoup
from flask import jsonify
from persiantools.jdatetime import JalaliDate, digits
from slugify import slugify

from exchange.models.coin_commercial import CoinCommercial, coins_commercial_schema
from exchange.models.coin_single import CoinSingle, coins_single_schema
from exchange.models.currency import Currency, currencies_schema
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
    urls = [
        'https://tgju.org/currency',
        'https://www.tgju.org/currency-minor'
    ]

    currency = []

    for url in urls:
        resp = requests.get(url)
        html = BeautifulSoup(resp.text, 'html.parser')

        tables = html.find_all('table', class_='market-table')

        for table in tables:
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')

            for row in rows:
                field = row.findChildren(['th', 'td'], recursive=True)

                title = field[0].text.strip()
                alpha2 = str(field[0].find('span').attrs['class'][1].replace('flag-', '')).upper()
                alpha3 = 'USD' if row['data-market-row'] == 'price_dollar_rl' \
                    else row['data-market-row'].replace('price_', '').upper()
                country = pycountry.countries.get(alpha_2=alpha2)
                live_price = field[1].text.strip()
                change = field[2].text.strip()
                min_price = field[3].text.strip()
                max_price = field[4].text.strip()
                updated_at = field[5].text.strip()

                rate_at = None

                try:
                    t = time.strptime(digits.fa_to_en(field[5].text.strip()), '%H:%M:%S')
                    rate_at = str('Today: ') + str(t.tm_hour) + ':' + str(t.tm_min) + ':' + str(t.tm_sec)
                except ValueError:
                    today = JalaliDate.today()
                    check_mouth = (re.split(r'\s', field[5].text))
                    mouth_day = int(check_mouth[0])
                    mouth_name = check_mouth[1]

                    if str(mouth_name) in mouth_names:
                        rate_at = JalaliDate(today.year, int(mouth_names[mouth_name]), mouth_day).strftime("%m/%d")

                if 'high' in field[2].find('span').attrs['class']:
                    sign = '+ '
                elif 'low' in field[2].find('span').attrs['class']:
                    sign = '- '
                else:
                    sign = ''

                if country or alpha3 == 'EUR':
                    currency.append({
                        "title": title,
                        "codes": [{
                            "alpha2": alpha2,
                            "alpha3": alpha3
                        }],
                        "country": country.name if country else 'EUR',
                        "prices": [{
                            "live": live_price,
                            "change": str(sign) + change,
                            "min": min_price,
                            "max": max_price
                        }],
                        "time": rate_at
                    })

    return currency


def fetch_coin():
    urls = [
        'https://www.tgju.org/coin'
    ]

    dump_coin_single = []
    dump_coin_commercial = []

    for url in urls:
        resp = requests.get(url)
        html = BeautifulSoup(resp.text, 'html.parser')

        tables = html.find_all('table', class_='market-table')

        coins_name = [
            'New Coin',
            'Old Coin',
            'Coin / Half',
            'Coin / Quarter',
            'Coin / Gram'
        ]

        for i, item in enumerate(tables, start=0):
            if i < 2:
                tbody = item.find('tbody')
                rows = tbody.find_all('tr')

                for coin_index, row in enumerate(rows, start=0):
                    field = row.findChildren(['th', 'td'], recursive=False)
                    title = coins_name[coin_index]
                    live_price = field[1].text.strip()
                    change = field[2].text.strip()
                    min_price = field[3].text.strip()
                    max_price = field[4].text.strip()
                    updated_at = field[5].text.strip()

                    rate_at = None

                    try:
                        t = time.strptime(digits.fa_to_en(field[5].text.strip()), '%H:%M:%S')
                        rate_at = str('Today: ') + str(t.tm_hour) + ':' + str(t.tm_min) + ':' + str(t.tm_sec)
                    except ValueError:
                        today = JalaliDate.today()
                        check_mouth = (re.split(r'\s', field[5].text))
                        mouth_day = int(check_mouth[0])
                        mouth_name = check_mouth[1]

                        if str(mouth_name) in mouth_names:
                            rate_at = JalaliDate(today.year, int(mouth_names[mouth_name]), mouth_day).strftime(
                                "%m/%d")

                    if 'high' in field[2].find('span').attrs['class']:
                        sign = '+ '
                    elif 'low' in field[2].find('span').attrs['class']:
                        sign = '- '
                    else:
                        sign = ''

                    if i == 0:
                        dump_coin_single.append({
                            "title": title,
                            "prices": [{
                                "live": live_price,
                                "change": str(sign) + change,
                                "min": min_price,
                                "max": max_price
                            }],
                            "time": rate_at
                        })
                    elif i == 1:
                        dump_coin_commercial.append({
                            "title": title,
                            "prices": [{
                                "live": live_price,
                                "change": str(sign) + change,
                                "min": min_price,
                                "max": max_price
                            }],
                            "time": rate_at
                        })
            else:
                break

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
            rate_currency = Currency(title=currency['title'],
                                     alpha2=currency['codes'][0]['alpha2'],
                                     alpha3=currency['codes'][0]['alpha3'],
                                     country=currency['country'],
                                     price=currency['prices'][0]['live'],
                                     change=currency['prices'][0]['change'],
                                     min=currency['prices'][0]['min'],
                                     max=currency['prices'][0]['max'],
                                     updated_at=currency['time']
                                     )
            db.session.add(rate_currency)

        for coin in data_coin[0]:
            rate_coin_single = CoinSingle(
                title=coin['title'],
                slug=slugify(coin['title']),
                price=coin['prices'][0]['live'],
                change=coin['prices'][0]['change'],
                min=coin['prices'][0]['min'],
                max=coin['prices'][0]['max'],
                updated_at=coin['time']
            )
            db.session.add(rate_coin_single)

        for coin in data_coin[1]:
            rate_coin_commercial = CoinCommercial(
                title=coin['title'],
                slug=slugify(coin['title']),
                price=coin['prices'][0]['live'],
                change=coin['prices'][0]['change'],
                min=coin['prices'][0]['min'],
                max=coin['prices'][0]['max'],
                updated_at=coin['time']
            )
            db.session.add(rate_coin_commercial)

        db.session.commit()

        return jsonify(message="success", status=200,
                       currency=data_currency, coin_single=data_coin[0], coin_commercial=data_coin[1]), 200


def get_currencies(limit=None):
    if limit:
        currencies = Currency.query.limit(limit).all()
    else:
        currencies = Currency.query.all()

    data = currencies_schema.dump(currencies)

    return data


def get_coin_single(limit=None):
    if limit:
        coins = CoinSingle.query.limit(limit).all()
    else:
        coins = CoinSingle.query.all()

    data = coins_single_schema.dump(coins)

    return data


def get_coin_commercial(limit=None):
    if limit:
        coins = CoinCommercial.query.limit(limit).all()
    else:
        coins = CoinCommercial.query.all()

    data = coins_commercial_schema.dump(coins)

    return data
