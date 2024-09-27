from init import db, ma
from marshmallow import fields

class Watchlist_Auction(db.Model):
    # Many to many relationship between Watchlist and Auction models
    __tablename__ = "watchlists_auctions"
    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey("watchlists.id"), nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey("auctions.id"), nullable=False)

    # Foreign key relationship to Watchlist model
    watchlist = db.relationship("Watchlist", back_populates="watchlists_auctions")
    # Foreign key relationship to Auction model
    auction = db.relationship("Auction", back_populates = "watchlists_auctions")

class Watchlist_AuctionSchema(ma.Schema):
    # Watchlist fields to include in the serialized output, only including id, title, description, and watchlists_auctions
    watchlist = fields.Nested("WatchlistSchema", exclude=["watchlists_auctions"])
    # Auction fields to include in the serialized output, only including id, title, description, status, and current_price
    auction = fields.Nested("AuctionSchema", exclude=["watchlists_auctions"])
    # Meta class to define the fields to include in the serialized output
    class Meta:
        fields = ("watchlist", "auction")

watchlist_Auctionschema = Watchlist_AuctionSchema()
watchlists_Auctionschema = Watchlist_AuctionSchema(many=True)