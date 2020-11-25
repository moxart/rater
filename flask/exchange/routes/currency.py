from flask import Blueprint, render_template

from exchange._helpers import get_currencies

bp_currency = Blueprint('bp_currency', __name__, url_prefix='/exchange')


@bp_currency.route('/currency/all', methods=['GET'])
def currency_all():
    data = get_currencies()
    return render_template('currency/currency-all.html', currency=data)
