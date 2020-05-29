from rater import db, ma


class CoinSingle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50))
    price = db.Column(db.Integer, nullable=False)
    change = db.Column(db.String)
    min = db.Column(db.Integer)
    max = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)

    def __repr__(self):
        return '<CoinSingle %r>' % self.title


class CoinSingleSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "title", "slug", "price", "change", "min", "max", "updated_at")


coin_single_schema = CoinSingleSchema()
coins_single_schema = CoinSingleSchema(many=True)

