from init import db, ma
from marshmallow import fields

class Watchlist(db.Model):
    __tablename__ = "watchlists"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    user = db.relationship("User", back_populates="watchlists")
    watchlists_auctions = db.relationship("Watchlist_Auction", back_populates="watchlist")

class WatchlistSchema(ma.Schema):
    watchlists_auctions = fields.List(fields.Nested("Watchlist_AuctionSchema",only=["auction"]))
    class Meta:
        fields = ("id", "user_id", "title", "description", "watchlists_auctions")

watchlist_schema = WatchlistSchema()
watchlists_schema = WatchlistSchema(many=True)