from flask import Blueprint, request, jsonify
from rater.models.currency import Currency, currency_schema, currencies_schema

bp_currency_api = Blueprint('bp_currency_api', __name__, url_prefix='/rates/api')


@bp_currency_api.route('/currency', methods=['GET'])
def api_currency():
    if request.method == 'GET':
        data = []

        currencies = Currency.query.all()
        dump = currencies_schema.dump(currencies)

        for item in dump:
            data.append({
                "title": item['title'],
                "codes": [{
                    "alpha2": item['alpha2'],
                    "alpha3": item['alpha3']
                }],
                "country": item['country'],
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


@bp_currency_api.route('/currency/<string:code>')
def api_currency_by(code):
    if request.method == 'GET':
        data = []

        currency = Currency.query.filter_by(alpha3=code.upper()).first()

        if not currency:
            return jsonify(message="Not Found", status=404)

        dump = currency_schema.dump(currency)

        data.append({
            "title": dump['title'],
            "codes": [{
                "alpha2": dump['alpha2'],
                "alpha3": dump['alpha3']
            }],
            "country": dump['country'],
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
