from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.auction import Auction, auction_schema, auctions_schema
from init import bcrypt, db
from datetime import datetime

auction_bp = Blueprint("auctions", __name__, url_prefix="/auctions")

@auction_bp.route("/")
def get_all_auctions():
    stmt = db.select(Auction)
    auctions = db.session.scalars(stmt)
    return auctions_schema.dump(auctions)

@auction_bp.route("/<int:auction_id>")
def get_auction(auction_id):
    stmt = db.select(Auction).filter_by(id=auction_id)
    auction = db.session.scalar(stmt)
    if auction:
        return auction_schema.dump(auction)
    else:
        return {"Error": f"Card id {auction_id} not found"}, 400

@auction_bp.route("/", methods=["POST"])
@jwt_required()
def create_auction():
    try:
        body = request.get_json()

        auction = Auction (
            created_user_id = get_jwt_identity(),
            title = body.get("title"),
            description = body.get("description"),
            current_price = body.get("starting_price"),
            status = "In Progress",
            created_at = datetime.now()

        )

        db.session.add(auction)
        db.session.commit()

        return auction_schema.dump(auction), 200
    
    #except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"Error": f"Missing required field: {err.orig.diag.column_name}"}, 400
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"Error": f"Field not unique"}, 400
    finally:
        pass