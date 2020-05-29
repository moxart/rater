from flask import Blueprint, request, jsonify
from slugify import slugify

from rater.models.coin_single import CoinSingle, coin_single_schema, coins_single_schema
from rater.models.coin_commercial import CoinCommercial, coin_commercial_schema, coins_commercial_schema

bp_coin_api = Blueprint('bp_coin_api', __name__, url_prefix='/rates/api')


@bp_coin_api.route('/coin', methods=['GET'])
def api_coin_all():
    if request.method == 'GET':
        dump_coin_single = []
        dump_coin_commercial = []

        single = CoinCommercial.query.all()
        dump_single = coins_commercial_schema.dump(single)

        for item in dump_single:
            dump_coin_single.append({
                "title": item['title'],
                "prices": [{
                    "live": item['price'],
                    "change": item['change'],
                    "min": item['min'],
                    "max": item['max']
                }],
                "time": item['updated_at']
            })

        commercial = CoinCommercial.query.all()
        dump_commercial = coins_commercial_schema.dump(commercial)

        for item in dump_commercial:
            dump_coin_commercial.append({
                "title": item['title'],
                "prices": [{
                    "live": item['price'],
                    "change": item['change'],
                    "min": item['min'],
                    "max": item['max']
                }],
                "time": item['updated_at']
            })

        dumper = [dump_single, dump_commercial]

        return jsonify(message="success", status=200, data=dumper)
    return jsonify(message="Unsupported Method")


@bp_coin_api.route('/coin/single', methods=['GET'])
def api_coin_single():
    if request.method == 'GET':
        data = []

        coins = CoinSingle.query.all()
        dump = coins_single_schema.dump(coins)

        for item in dump:
            data.append({
                "title": item['title'],
                "prices": [{
                    "live": item['price'],
                    "change": item['change'],
                    "min": item['min'],
                    "max": item['max']
                }],
                "time": item['updated_at']
            })

        return jsonify(message="success", status=200, data=data)
    return jsonify(message="Unsupported Method")


@bp_coin_api.route('/coin/single/<string:code>')
def api_coin_single_by(code):
    if request.method == 'GET':
        data = []

        coin = CoinSingle.query.filter_by(slug=slugify(code.upper())).first()

        if not coin:
            return jsonify(message="Not Found", status=404)

        dump = coin_single_schema.dump(coin)

        data.append({
            "title": dump['title'],
            "prices": [{
                "live": dump['price'],
                "change": dump['change'],
                "min": dump['min'],
                "max": dump['max']
            }],
            "time": dump['updated_at']
        })

        return jsonify(message="Success", status=200, data=data)

    return jsonify(message="Unsupported Method")


@bp_coin_api.route('/coin/commercial', methods=['GET'])
def api_coin_commercial():
    if request.method == 'GET':
        data = []

        coins = CoinCommercial.query.all()
        dump = coins_commercial_schema.dump(coins)

        for item in dump:
            data.append({
                "title": item['title'],
                "prices": [{
                    "live": item['price'],
                    "change": item['change'],
                    "min": item['min'],
                    "max": item['max']
                }],
                "time": item['updated_at']
            })

        return jsonify(message="success", status=200, data=data)
    return jsonify(message="Unsupported Method")


@bp_coin_api.route('/coin/commercial/<string:code>')
def api_coin_commercial_by(code):
    if request.method == 'GET':
        data = []

        coin = CoinCommercial.query.filter_by(slug=slugify(code.upper())).first()

        if not coin:
            return jsonify(message="Not Found", status=404)

        dump = coin_commercial_schema.dump(coin)

        data.append({
            "title": dump['title'],
            "prices": [{
                "live": dump['price'],
                "change": dump['change'],
                "min": dump['min'],
                "max": dump['max']
            }],
            "time": dump['updated_at']
        })

        return jsonify(message="Success", status=200, data=data)

    return jsonify(message="Unsupported Method")
