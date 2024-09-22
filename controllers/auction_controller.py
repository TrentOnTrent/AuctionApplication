from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.auction import Auction, auction_schema, auctions_schema
from models.user import User
from init import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from controllers.bids_controller import bids_bp
from controllers.watch_controller import watch_bp
from utils import auth_as_admin_decorator

auction_bp = Blueprint("auctions", __name__, url_prefix="/auctions")
auction_bp.register_blueprint(watch_bp)
auction_bp.register_blueprint(bids_bp)


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
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"Error": f"Missing required field: {err.orig.diag.column_name}"}, 400
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"Error": f"Field not unique"}, 400
        
@auction_bp.route("/<int:auction_id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_auction(auction_id):
    stmt = db.select(Auction).filter_by(id=auction_id)
    auction = db.session.scalar(stmt)
    current_user = get_jwt_identity()
    userstmt = db.select(User).filter_by(id=current_user)
    current_user_admin = db.session.scalar(userstmt)
    if str(auction.created_user_id) != current_user and current_user_admin.admin_role == False:
        return {"Error": f"Not authorised to edit card id {auction_id}"}, 400
    
    if auction:
        body = request.get_json()
        auction.description = body.get("description") or auction.description
        auction.status = body.get("status") or auction.status
        db.session.add(auction)
        db.session.commit()
        return auction_schema.dump(auction)
    else:
        return {"Error": f"Card id {auction_id} not found"}, 404
    
@auction_bp.route("/<int:auction_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator()
def delete_auction(auction_id):
    stmt = db.select(Auction).filter_by(id=auction_id)
    auction = db.session.scalar(stmt)

    if auction:
        db.session.delete(auction)
        db.session.commit()
        return {"Success": f"Auction id {auction_id} deleted!"}, 200
    else:
        return {"Error": f"Auction id {auction_id} not found"}, 404