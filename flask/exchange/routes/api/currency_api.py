from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from exchange import create_app
from exchange.models.currency import Currency, currency_schema, currencies_schema
from exchange.models.mappers.currency_mapper import map_from_entity, map_from_entity_list

bp_currency_api = Blueprint(
    'bp_currency_api', __name__, url_prefix='/exchange/api')

app = create_app()

limiter = Limiter(
    app,
    key_func=get_remote_address
)


@bp_currency_api.route('/currency', methods=['GET'])
@limiter.limit("1000/day;100/minute")
def api_currency():
    if request.method == 'GET':

        currencies = Currency.query.all()
        dump = currencies_schema.dump(currencies)
        data = map_from_entity_list(dump)

        return jsonify(message="success", status=200, totalResults=len(data), data=data)

    return jsonify(message="Unsupported Method")


@bp_currency_api.route('/currency/<string:code>')
@limiter.limit("1000/day;100/minute")
def api_currency_by(code):
    if request.method == 'GET':

        currency = Currency.query.filter_by(alpha3=code.upper()).first()

        if not currency:
            return jsonify(message="Not Found", status=404)

        dump = currency_schema.dump(currency)
        data = map_from_entity(dump)

        return jsonify(message="Success", status=200, data=data)

    return jsonify(message="Unsupported Method")
