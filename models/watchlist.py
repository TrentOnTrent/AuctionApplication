from init import db, ma
from marshmallow import fields

class Watchlist(db.Model):
    __tablename__ = "watchlists"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    user = db.relationship("User", back_populates="watchlists")
    watchlists_auctions = db.relationship("Watchlist_Auction", back_populates="watchlists")

class WatchlistSchema(ma.Schema):

    class Meta:
        fields = ("id", "user_id", "title", "description")

watchlist_schema = WatchlistSchema()
watchlists_schema = WatchlistSchema(many=True)