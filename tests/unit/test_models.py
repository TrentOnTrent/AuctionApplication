from models.user import User
from models.auction import Auction
from models.bid import Bid
from models.watchlist import Watchlist
from models.watchlist_auction import Watchlist_Auction
from init import bcrypt

def test_new_user():
    user = User(email="unittest@test.com", username="unittest", password="unittestpassword")

    assert user.email == "unittest@test.com"
    assert user.username == "unittest"
    assert bcrypt.generate_password_hash(user.password) != "unittestpassword"