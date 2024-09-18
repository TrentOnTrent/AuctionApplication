from init import db, ma


class Auction(db.Model):
    __tablename__ = "auctions"
    id = db.Column(db.Integer, primary_key=True)
    created_user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.string, nullable=False)
    description = db.Column(db.string)
    status = db.Column(db.string)
    current_price = db.Column(db.float)
    created_at= db.column(db.DateTime)

    class UserSchema(ma.Schema):
        class Meta:
            fields = ("id", "created_user_id", "title", "description", "status", "current_price", "created_at")
    
    auction_schema = UserSchema()
    auctions_schema = UserSchema(many=True)