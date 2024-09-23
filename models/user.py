from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin_role = db.Column(db.Boolean)

    auctions = db.relationship("Auction", back_populates = "user", cascade="all, delete")
    bids = db.relationship("Bid", back_populates = "user", cascade="all, delete")
    watchlists = db.relationship("Watchlist", back_populates = "user", cascade="all, delete")

    
class UserSchema(ma.Schema):
    auctions = fields.List(fields.Nested("AuctionSchema", exclude=["user"]))
    bids = fields.List(fields.Nested("BidSchema", only=["created_at", "amount"]))
    
    class Meta:
        fields = ("id", "username", "email", "password", "admin_role", "auctions", "bids")

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(exclude=["password"], many=True)