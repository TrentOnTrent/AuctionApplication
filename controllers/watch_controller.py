from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.auction import Auction, auction_schema, auctions_schema
from models.user import User
from models.bid import Bid, bid_schema, bids_schema
from models.watchlist import Watchlist, watchlist_schema, watchlists_schema
from models.watchlist_auction import Watchlist_Auction, watchlist_Auctionschema
from init import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

watch_bp = Blueprint("watch", __name__, url_prefix="/<int:auction_id>/watch")
watchlist_bp = Blueprint("watchlist", __name__, url_prefix="/watchlist")

@watch_bp.route("/", methods=["POST"])
@jwt_required()
def create_watch(auction_id):
    body = request.get_json()
    stmt = db.select(Auction).filter_by(id=auction_id)
    auction = db.session.scalar(stmt)

    if not auction:
        return {"Error": f"Card id {auction_id} not found"}, 404
    
    user = get_jwt_identity()
    if int(user) == auction.created_user_id:
        return {"Error": "Cannot watch own auction"}, 400

    if auction.status != "In Progress":
        return {"Error": "Auction is not in progress"}, 400
    
    watchlist_id = body.get("watchlist")

    stmt = db.select(Watchlist).filter_by(id=watchlist_id)
    watchlist = db.session.scalar(stmt)
    
    if not watchlist:
        return {"Error": f"Watchlist id {watchlist_id} not found"}, 404

    watchlist_auction = Watchlist_Auction(
        watchlist_id = body.get("watchlist"),
        auction_id = auction_id
    )
    db.session.add(watchlist_auction)
    db.session.commit()

    return watchlist_Auctionschema(watchlist_auction), 200

@watchlist_bp.route("/")
@jwt_required()
def get_watchlists():
    user = get_jwt_identity()
    stmt = db.select(Watchlist).filter_by(user_id=user)
    watchlists = db.session.scalars(stmt)
    return watchlists_schema.dump(watchlists)
    