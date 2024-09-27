from init import db, ma
from marshmallow import fields

class Watchlist(db.Model):
    __tablename__ = "watchlists"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    # Foreign key relationship to User model
    user = db.relationship("User", back_populates="watchlists")
    # Foreign key relationship to Watchlist_Auction model, including cascading delete
    watchlists_auctions = db.relationship("Watchlist_Auction", back_populates="watchlist", cascade="all, delete")

class WatchlistSchema(ma.Schema):
    # Watchlist_Auction fields to include in the serialized output, only including auction
    watchlists_auctions = fields.List(fields.Nested("Watchlist_AuctionSchema",only=["auction"]))
    # Meta class to define the fields to include in the serialized output
    class Meta:
        fields = ("id", "user_id", "title", "description", "watchlists_auctions")

watchlist_schema = WatchlistSchema()
watchlists_schema = WatchlistSchema(many=True)