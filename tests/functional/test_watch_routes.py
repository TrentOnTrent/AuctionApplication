from init import db, ma, bcrypt, jwt
from models.auction import Auction
from models.watchlist import Watchlist
from models.user import User
from flask_jwt_extended import create_access_token

def test_create_watchlist(new_user, client, app):
    with app.app_context():
        with app.test_request_context():
            token = create_access_token(identity="1")
            headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/watchlist/", headers=headers, json={"title": "test watchlist", "description": "test watchlist description"})
    assert response.status_code == 200

def test_get_all_watchlists(app, client, new_user, new_watchlist):
    with app.app_context():
        with app.test_request_context():
            token = create_access_token(identity="1")
            headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/watchlist/", headers=headers)
    assert response.status_code == 200

def test_get_watchlist_by_id(app, client, new_user, new_watchlist):
    with app.app_context():
        with app.test_request_context():
            token = create_access_token(identity="1")
            headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/watchlist/1", headers=headers)
    assert response.status_code == 200

def test_add_auction_to_watchlist(app, client, new_user, new_auction, new_watchlist):
    with app.app_context():
        with app.test_request_context():
            # Creating second user
            user = User(email="unittest2@test.com", username="unittest2", password="unittestpassword2", admin_role=True)
            db.session.add(user)

            # Using second user (different to auction user)
            token = create_access_token(identity="2")
            headers = {"Authorization": f"Bearer {token}"}
            stmt = db.select(Auction).filter_by(id=1)
            auction = db.session.scalar(stmt)
            auction.status = "In Progress"
            db.session.add(auction)
            
            # Changing watchlist user to second user
            stmt = db.select(Watchlist).filter_by(id=1)
            watchlist = db.session.scalar(stmt)
            watchlist.user_id = 2
            db.session.add(watchlist)
            db.session.commit()

    response = client.post("/auctions/1/watch/", headers=headers, json={"watchlist": 1})
    assert response.status_code == 200

def test_delete_watchlist(app, client, new_user, new_watchlist):
    with app.app_context():
        with app.test_request_context():
            token = create_access_token(identity="1")
            headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/watchlist/1", headers=headers)
    assert response.status_code == 200


