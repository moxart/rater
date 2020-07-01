import os

from flask import Flask
from flask_compress import Compress
from flask_htmlmin import HTMLMIN
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
compress = Compress()
htmlmin = HTMLMIN()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    ma.init_app(app)
    compress.init_app(app)
    htmlmin.init_app(app)

    from exchange.routes import main
    from exchange.routes import currency
    from exchange.routes import coin
    from exchange.routes.api import currency_api
    from exchange.routes.api import coin_api

    app.register_blueprint(main.bp_main)
    app.register_blueprint(currency.bp_currency)
    app.register_blueprint(coin.bp_coin)

    app.register_blueprint(currency_api.bp_currency_api)
    app.register_blueprint(coin_api.bp_coin_api)

    with app.app_context():
        from .models.currency import Currency
        from .models.coin_single import CoinSingle
        from .models.coin_commercial import CoinCommercial

        db.create_all()

    return app
