from init import db, ma


class Auction(db.Model):
    __tablename__ = "auctions"
    id = db.Column(db.Integer, primary_key=True)
    created_user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    status = db.Column(db.String)
    current_price = db.Column(db.Float, nullable=False)
    created_at= db.Column(db.DateTime)

    class UserSchema(ma.Schema):
        class Meta:
            fields = ("id", "created_user_id", "title", "description", "status", "current_price", "created_at")
    
    auction_schema = UserSchema()
    auctions_schema = UserSchema(many=True)