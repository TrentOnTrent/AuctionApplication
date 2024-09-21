from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.auction import Auction, auction_schema, auctions_schema
from models.user import User
from models.bid import Bid, bid_schema, bids_schema
from init import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

bids_bp = Blueprint("bids", __name__, url_prefix="/<int:auction_id>/bids")

@bids_bp.route("/", methods=["POST"])
@jwt_required()
def create_bid(auction_id):
    body = request.get_json()
    stmt = db.select(Auction).filter_by(id=auction_id)
    auction = db.session.scalar(stmt)
    print (auction)

    if not auction:
        return {"Error": f"Card id {auction_id} not found"}, 404
    
    if auction.current_price > float(body.get("price")):
        return {"Error": "Bid price not higher than current price"}
    
    user = get_jwt_identity()
    if user == auction.created_user_id:
        return {"Error": "Cannot bid on own auction"}

    if auction.status != "In Progress":
        return {"Error": "Auction is not in progress"}
    
    bid = Bid(
        auction_id = auction_id,
        user_id = user,
        created_at = datetime.now(),
        amount = body.get("price")
    )

    db.session.add(bid)
    db.session.commit()

    return bid_schema.dump(bid), 200