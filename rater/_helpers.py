import requests
import re
import pycountry

from flask import jsonify
from slugify import slugify
from bs4 import BeautifulSoup
from rater.models.currency import Currency, currencies_schema
from rater.models.coin_single import CoinSingle, coins_single_schema
from rater.models.coin_commercial import CoinCommercial, coins_commercial_schema
from unidecode import unidecode
from . import db


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
                field = row.findChildren(['th', 'td'], recursive=False)

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

                if 'high' in field[2].find('span').attrs['class']:
                    sign = '+ '
                elif 'low' in field[2].find('span').attrs['class']:
                    sign = '- '
                else:
                    sign = ''
                print(alpha3)
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
                        "time": unidecode(updated_at) if re.search(':', updated_at) else "-"
                    })

    return currency


def fetch_coin():
    urls = [
        'https://english.tgju.net/coin'
    ]

    dump_coin_single = []
    dump_coin_commercial = []

    for url in urls:
        resp = requests.get(url)
        html = BeautifulSoup(resp.text, 'html.parser')

        tables = html.find_all('table', class_='market-table')

        for i, item in enumerate(tables, start=0):
            if i < 2:
                tbody = item.find('tbody')
                rows = tbody.find_all('tr')

                for row in rows:
                    field = row.findChildren(['th', 'td'], recursive=False)

                    title = field[0].text.strip()
                    live_price = field[1].text.strip()
                    change = field[2].text.strip()
                    min_price = field[3].text.strip()
                    max_price = field[4].text.strip()
                    updated_at = field[5].text.strip()

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
                            "time": updated_at
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
                            "time": updated_at
                        })

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
