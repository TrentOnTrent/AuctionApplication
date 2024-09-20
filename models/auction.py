from init import db, ma
from marshmallow import fields

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

    class AuctionSchema(ma.Schema):
        user = fields.Nested("UserSchema", only=["id", "email", "username"])

        class Meta:
            fields = ("id", "user", "title", "description", "status", "current_price", "created_at")
    
    auction_schema = AuctionSchema()
    auctions_schema = AuctionSchema(many=True)