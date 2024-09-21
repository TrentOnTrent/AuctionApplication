from flask import Blueprint, request
from models.auction import Auction, auction_schema, auctions_schema
from init import bcrypt, db

auction_bp = Blueprint("auctions", __name__, url_prefix="/auctions")

@auction_bp.route("/")
def get_all_auctions():
    stmt = db.select(Auction)
    auctions = db.session.scalars(stmt)
    return auctions_schema.dump(auctions)