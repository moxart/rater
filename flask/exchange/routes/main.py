from flask import Blueprint, render_template

from exchange._helpers import get_currencies

bp_main = Blueprint('bp_main', __name__)


@bp_main.route('/exchange', methods=['GET'])
def homepage():
    data_currency = get_currencies(10)
    return render_template('index.html', currency=data_currency)


@bp_main.route('/api', methods=['GET'])
def api():
    return render_template('api/index.html')
