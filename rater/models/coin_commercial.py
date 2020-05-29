from rater import db, ma


class CoinCommercial(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50))
    price = db.Column(db.Integer, nullable=False)
    change = db.Column(db.String)
    min = db.Column(db.Integer)
    max = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)

    def __repr__(self):
        return '<CoinCommercial %r>' % self.title


class CoinCommercialSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "title", "slug", "price", "change", "min", "max", "updated_at")


coin_commercial_schema = CoinCommercialSchema()
coins_commercial_schema = CoinCommercialSchema(many=True)
