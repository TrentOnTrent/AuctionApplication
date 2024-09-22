from init import db, ma
from marshmallow import fields

class Watchlist_Auction(db.Model):
    __tablename__ = "watchlists_auctions"
    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey("watchlists.id"), nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey("auctions.id"), nullable=False)

    watchlist = db.relationship("Watchlist", back_populates="watchlists_auctions")
    auction = db.relationship("Auction", back_populates = "watchlists_auctions")

class Watchlist_AuctionSchema(ma.Schema):
    watchlist = fields.Nested("WatchlistSchema", exclude=["watchlists_auctions"])
    auction = fields.Nested("AuctionSchema", exclude=["watchlists_auctions"])
    class Meta:
        fields = ("watchlist", "auction")

watchlist_Auctionschema = Watchlist_AuctionSchema()
watchlists_Auctionschema = Watchlist_AuctionSchema(many=True)