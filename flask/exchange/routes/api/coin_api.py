from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from slugify import slugify

from exchange import create_app
from exchange.models.coin_commercial import CoinCommercial, coin_commercial_schema, coins_commercial_schema
from exchange.models.coin_single import CoinSingle, coin_single_schema, coins_single_schema
from exchange.models.mappers.coin_mapper import map_from_entity, map_from_entity_list
from exchange import constant

bp_coin_api = Blueprint('bp_coin_api', __name__, url_prefix='/exchange/api')

app = create_app()

limiter = Limiter(
    app,
    key_func=get_remote_address
)


@bp_coin_api.route('/coin', methods=['GET'])
@limiter.limit("1000/day;100/minute")
def api_coin_all():
    if request.method == 'GET':

        single = CoinCommercial.query.all()
        dump_single = coins_commercial_schema.dump(single)
        dump_coin_single = map_from_entity_list(dump_single)

        commercial = CoinCommercial.query.all()
        dump_commercial = coins_commercial_schema.dump(commercial)
        dump_coin_commercial = map_from_entity_list(dump_commercial)

        dumper = {
            "single": dump_single,
            "commercial": dump_commercial
        }

        return jsonify(message=constant.MESSAGE_SUCCESS, status=200,
                       totalResults=len(dump_coin_single + dump_coin_commercial), data=dumper)
    return jsonify(message=constant.MESSAGE_UNSUPPORTED_METHOD)


@bp_coin_api.route('/coin/single', methods=['GET'])
@limiter.limit("1000/day;100/minute")
def api_coin_single():
    if request.method == 'GET':

        coins = CoinSingle.query.all()
        dump = coins_single_schema.dump(coins)
        data = map_from_entity_list(dump)

        return jsonify(message=constant.MESSAGE_SUCCESS, status=200, totalResults=len(data), data=data)
    return jsonify(message=constant.MESSAGE_UNSUPPORTED_METHOD)


@bp_coin_api.route('/coin/single/<string:code>')
@limiter.limit("1000/day;100/minute")
def api_coin_single_by(code):
    if request.method == 'GET':

        coin = CoinSingle.query.filter_by(slug=slugify(code.upper())).first()

        if not coin:
            return jsonify(message=constant.MESSAGE_NOT_FOUND, status=404)

        dump = coin_single_schema.dump(coin)
        data = map_from_entity(dump)

        return jsonify(message=constant.MESSAGE_SUCCESS, status=200, data=data)

    return jsonify(message=constant.MESSAGE_UNSUPPORTED_METHOD)


@bp_coin_api.route('/coin/commercial', methods=['GET'])
@limiter.limit("1000/day;100/minute")
def api_coin_commercial():
    if request.method == 'GET':

        coins = CoinCommercial.query.all()
        dump = coins_commercial_schema.dump(coins)
        data = map_from_entity_list(dump)

        return jsonify(message=constant.MESSAGE_SUCCESS, status=200, totalResults=len(data), data=data)
    return jsonify(message=constant.MESSAGE_UNSUPPORTED_METHOD)


@bp_coin_api.route('/coin/commercial/<string:code>')
@limiter.limit("1000/day;100/minute")
def api_coin_commercial_by(code):
    if request.method == 'GET':

        coin = CoinCommercial.query.filter_by(
            slug=slugify(code.upper())).first()

        if not coin:
            return jsonify(message=constant.MESSAGE_NOT_FOUND, status=404)

        dump = coin_commercial_schema.dump(coin)
        data = map_from_entity(dump)

        return jsonify(message=constant.MESSAGE_SUCCESS, status=200, data=data)

    return jsonify(message=constant.MESSAGE_UNSUPPORTED_METHOD)
