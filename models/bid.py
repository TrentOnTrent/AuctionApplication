from init import db, ma


class Bid(db.Model):
    __tablename__ = "bids"
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    created_at= db.Column(db.DateTime)
    amount = db.Column(db.Float)

    class UserSchema(ma.Schema):
        class Meta:
            fields = ("id", "auction_id", "user_id", "created_at", "amount")
    
    user_schema = UserSchema()
    users_schema = UserSchema(many=True)