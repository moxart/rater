from flask import Blueprint, render_template, jsonify, make_response
from rater._helpers import get_currencies, save_to_database

bp_currency = Blueprint('bp_currency', __name__, url_prefix='/rates')


@bp_currency.route('/currency/all', methods=['GET'])
def currency_all():
    data = get_currencies()
    return render_template('currency/currency-all.html', currency=data)


@bp_currency.route('/currency/update-database', methods=['GET'])
def update_database():
    if save_to_database():
        return jsonify(message='database has been updated successfully')
