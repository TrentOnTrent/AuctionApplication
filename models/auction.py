from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf


VALID_STATUSES = ("In Progress", "Completed")

class Auction(db.Model):
    __tablename__ = "auctions"
    id = db.Column(db.Integer, primary_key=True)
    created_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    status = db.Column(db.String)
    current_price = db.Column(db.Float, nullable=False)
    created_at= db.Column(db.DateTime)
    # Foreign key relationship to User model
    user = db.relationship("User", back_populates = "auctions")
    # Foreign key relationship to Bid model, including cascading delete
    bids = db.relationship("Bid", back_populates = "auction", cascade="all, delete")
    # Foreign key relationship to Watchlist_Auction model, including cascading delete
    watchlists_auctions = db.relationship("Watchlist_Auction", back_populates = "auction", cascade="all, delete")

class AuctionSchema(ma.Schema):
    # Bid fields to include in the serialized output, only including created_at and amount
    bids = fields.List(fields.Nested("BidSchema", only=["created_at", "amount"]))
    # User fields to include in the serialized output, only including id, email, and username
    user = fields.Nested("UserSchema", only=["id", "email", "username"])
    # Watchlist_Auction fields to include in the serialized output, only including watchlist
    watchlists_auctions = fields.List(fields.Nested("Watchlist_AuctionSchema", only=["watchlist"]))
    # status field to include in the serialized output, validating against a list of valid statuses
    status = fields.String(validate=OneOf(VALID_STATUSES))
    # Meta class to define the fields to include in the serialized output
    class Meta:   
        fields = ("id", "user", "bids", "title", "description", "status", "current_price", "created_at", "watchlists_auctions")

auction_schema = AuctionSchema()
auctions_schema = AuctionSchema(many=True)