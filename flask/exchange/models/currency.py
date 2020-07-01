from exchange import db, ma


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    alpha2 = db.Column(db.String(50), nullable=False)
    alpha3 = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    change = db.Column(db.String)
    min = db.Column(db.Integer)
    max = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)

    def __repr__(self):
        return '<Currency %r>' % self.alpha3


class CurrencySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "title", "alpha2", "alpha3", "country", "price", "change", "min", "max", "updated_at")


currency_schema = CurrencySchema()
currencies_schema = CurrencySchema(many=True)
