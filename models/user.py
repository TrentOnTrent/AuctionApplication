from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin_role = db.Column(db.Boolean)
    # Foreign key relationship to Auction model, including cascading delete
    auctions = db.relationship("Auction", back_populates = "user", cascade="all, delete")
    # Foreign key relationship to Bid model, including cascading delete
    bids = db.relationship("Bid", back_populates = "user", cascade="all, delete")
    # Foreign key relationship to Watchlist model, including cascading delete
    watchlists = db.relationship("Watchlist", back_populates = "user", cascade="all, delete")

    
class UserSchema(ma.Schema):
    # Auction fields to include in the serialized output, only including id, title, description, status, and current_price
    auctions = fields.List(fields.Nested("AuctionSchema", exclude=["user"]))
    # Bid fields to include in the serialized output, only including created_at and amount
    bids = fields.List(fields.Nested("BidSchema", only=["created_at", "amount"]))
    # User fields to include in the serialized output, confirming email format
    email = fields.String(required=True, validate=Regexp("^\\S+@\\S+\\.\\S+$", error="Invalid Email Format."))
    
    # Meta class to define the fields to include in the serialized output
    class Meta:
        fields = ("id", "username", "email", "password", "admin_role", "auctions", "bids")

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(exclude=["password"], many=True)