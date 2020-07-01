from flask import Blueprint, render_template

from exchange._helpers import get_coin_single, get_coin_commercial

bp_coin = Blueprint('bp_coin', __name__, url_prefix='/')


@bp_coin.route('/coin', methods=['GET'])
def coin():
    data_coin_single = get_coin_single()
    return render_template('coin/index.html', coin_single=data_coin_single)


@bp_coin.route('/coin/all', methods=['GET'])
def coin_all():
    data_coin_single = get_coin_single()
    data_coin_commercial = get_coin_commercial()

    return render_template('coin/coin-all.html',
                           coin_single=data_coin_single, coin_commercial=data_coin_commercial)
