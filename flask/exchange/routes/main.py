from flask import Blueprint, render_template, jsonify

from exchange._helpers import get_currencies, save_to_database
from exchange import constant

bp_main = Blueprint('bp_main', __name__)


@bp_main.route('/exchange', methods=['GET'])
def homepage():
    data_currency = get_currencies(10)
    return render_template('index.html', currency=data_currency)


@bp_main.route('/exchange/api', methods=['GET'])
def api():
    return render_template('api/index.html')


@bp_main.route('/exchange/update-database', methods=['GET'])
def update_database():
    if save_to_database():
        return jsonify(message=constant.MESSAGE_SUCCESS_DB)
