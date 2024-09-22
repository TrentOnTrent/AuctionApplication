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

    user = db.relationship("User", back_populates = "auctions")
    bids = db.relationship("Bid", back_populates = "auction")

    watchlists_auctions = db.relationship("Watchlist_Auction", back_populates = "auctions")

class AuctionSchema(ma.Schema):
    bids = fields.List(fields.Nested("BidSchema", only=["created_at", "amount"]))
    user = fields.Nested("UserSchema", only=["id", "email", "username"])
    
    watchlists_auctions = fields.List(fields.Nested("Watchlist_AuctionSchema"))
    status = fields.String(validate=OneOf(VALID_STATUSES))
    class Meta:   
        fields = ("id", "user", "bids", "title", "description", "status", "current_price", "created_at", "watchlist_auctions")

auction_schema = AuctionSchema()
auctions_schema = AuctionSchema(many=True)