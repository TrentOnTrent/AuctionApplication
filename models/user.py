from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin_role = db.Column(db.Boolean)

    auctions = db.relationship("Auction", back_populates = "user")
    
class UserSchema(ma.Schema):
    auctions = fields.List(fields.Nested("AuctionSchema", exclude=["user"]))
    
    class Meta:
        fields = ("id", "username", "password", "admin_role", "watchlist")

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])