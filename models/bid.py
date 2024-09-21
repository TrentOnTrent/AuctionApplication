from init import db, ma
from marshmallow import fields

class Bid(db.Model):
    __tablename__ = "bids"
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey("auctions.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime)
    amount = db.Column(db.Float, nullable=False)

    user = db.relationship("User", back_populates="bids")
    auction = db.relationship("Auction", back_populates="bids")
    
class BidSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["id", "email", "username"])
    auction = fields.Nested("AuctionSchema")

    class Meta:
        fields = ("id", "auction", "user", "created_at", "amount")

bid_schema = BidSchema()
bids_schema = BidSchema(many=True)