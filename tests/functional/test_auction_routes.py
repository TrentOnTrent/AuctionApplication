from init import db, ma, bcrypt, jwt
from models.auction import Auction
from flask_jwt_extended import create_access_token

def test_get_all_auctions(client):
    response = client.get("/auctions/")
    assert response.status_code == 200
    assert response.json == []

def test_get_auction_by_id(new_user, new_auction, client):
    response = client.get("/auctions/1")
    assert response.status_code == 200  

def test_create_auction(new_user, new_auction, client, app):
    with app.app_context():
        with app.test_request_context():
            token = create_access_token(identity="1")
            headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/auctions/", headers=headers, json={"title": "test auction", "description": "test auction description", "starting_price": 100, "status": "test status"})
    assert response.status_code == 200

def test_edit_auction(new_user, new_auction, client, app):
    with app.app_context():
        with app.test_request_context():
            token = create_access_token(identity="1")
            headers = {"Authorization": f"Bearer {token}"}
    response = client.put("/auctions/1", headers=headers, json={"description": "test edit auction description", "status": "test edit status"})
    assert response.status_code == 200
    stmt = db.select(Auction).filter_by(id=1)
    test_auction = db.session.scalar(stmt)
    assert test_auction.description == "test edit auction description"
    assert test_auction.status == "test edit status"

def test_delete_auction(new_user, new_auction, client, app):
    with app.app_context():
        with app.test_request_context():
            token = create_access_token(identity="1")
            headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/auctions/1", headers=headers)
    assert response.status_code == 200