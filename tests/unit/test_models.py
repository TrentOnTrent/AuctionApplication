import os
from models.user import User
from models.auction import Auction
from models.bid import Bid
from models.watchlist import Watchlist
from models.watchlist_auction import Watchlist_Auction
from init import bcrypt, db

def test_new_user(app, new_user):
    with app.app_context():
        stmt = db.select(User).filter_by(id=1)
        new_user = db.session.scalar(stmt)
        assert new_user.email == "unittest@test.com"
        assert new_user.username == "unittest"
        assert bcrypt.generate_password_hash(new_user.password) != "unittestpassword"

def test_new_auction(app, new_user, new_auction):
    with app.app_context():
        stmt = db.select(Auction).filter_by(id=1)
        new_auction = db.session.scalar(stmt)
        assert new_auction.title == "test auction"
        assert new_auction.description == "test auction description"
        assert new_auction.status == "test status"
        assert new_auction.current_price == 100
    
def test_new_bid(app, new_user, new_auction, new_bid):
    with app.app_context():
        stmt = db.select(Bid).filter_by(id=1)
        new_bid = db.session.scalar(stmt)
        assert new_bid.amount == 100
        assert new_bid.auction_id == 1
        assert new_bid.user_id == 1