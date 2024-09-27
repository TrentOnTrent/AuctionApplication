from init import db, ma
from marshmallow import fields

class Bid(db.Model):
    __tablename__ = "bids"
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey("auctions.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime)
    amount = db.Column(db.Float, nullable=False)
    # Foreign key relationship to User model
    user = db.relationship("User", back_populates="bids")
    # Foreign key relationship to Auction model
    auction = db.relationship("Auction", back_populates="bids")
    
class BidSchema(ma.Schema):
    # User fields to include in the serialized output, only including id, email, and username
    user = fields.Nested("UserSchema", only=["id", "email", "username"])
    # Auction fields to include in the serialized output, only including id, title, description, status, and current_price
    auction = fields.Nested("AuctionSchema")
    # Meta class to define the fields to include in the serialized output
    class Meta:
        fields = ("id", "auction", "user", "created_at", "amount")

bid_schema = BidSchema()
bids_schema = BidSchema(many=True)