from init import db, ma
from marshmallow import fields

class Watchlist_Auction(db.Model):
    __tablename__ = "watchlists_auctions"
    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey("watchlists.id"), nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey("auctions.id"), nullable=False)

    watchlists = db.relationship("Watchlist", back_populates="watchlists_auctions")
    auctions = db.relationship("Auction", back_populates = "watchlists_auctions")

class Watchlist_AuctionSchema(ma.Schema):
    watchlist = fields.Nested("WatchlistSchema")
    auction = fields.Nested("AuctionSchema")
    class Meta:
        fields = ("watchlist", "auction")

watchlist_Auctionschema = Watchlist_AuctionSchema()
watchlists_Auctionschema = Watchlist_AuctionSchema(many=True)