import os
from models.user import User
from models.auction import Auction
from models.bid import Bid
from models.watchlist import Watchlist
from models.watchlist_auction import Watchlist_Auction
from init import bcrypt, db

def test_new_user(app, new_user):
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
        stmt = db.select(User).filter_by(id=1)
        new_user = db.session.scalar(stmt)
        assert new_user.email == "unittest@test.com"
        assert new_user.username == "unittest"
        assert bcrypt.generate_password_hash(new_user.password) != "unittestpassword"
    