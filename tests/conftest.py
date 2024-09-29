import pytest
import os
from main import create_app
from init import db, ma, bcrypt, jwt
from models.user import User
from models.auction import Auction
from models.bid import Bid
from models.watchlist import Watchlist
from flask import Flask
from controllers.auth_controller import auth_bp
from controllers.auction_controller import auction_bp
from controllers.bids_controller import bids_bp
from controllers.watch_controller import watch_bp, watchlist_bp

@pytest.fixture()
def app():
    app = Flask(__name__)
    with app.app_context():
        app.config['TESTING']= True
        app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get("TEST_DATABASE_URI")
        app.config['SECRET_KEY']= os.environ.get("JWT_SECRET_KEY")
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        # Creates tables for test database
        db.create_all()
    yield app
    with app.app_context():
        # Drops tables for test database
        db.drop_all()

@pytest.fixture()
def client(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(auction_bp)
    app.register_blueprint(bids_bp)
    app.register_blueprint(watch_bp)
    app.register_blueprint(watchlist_bp)
    with app.test_client() as client:
        yield client

@pytest.fixture()
def new_user(app):
    user = User(email="unittest@test.com", username="unittest", password="unittestpassword", admin_role=True)
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    return user

@pytest.fixture()
def new_watchlist(app):
    with app.app_context():
        stmt = db.select(User).filter_by(id=1)
        user = db.session.scalar(stmt)
        watchlist = Watchlist(title="test watchlist", description="test watchlist description", user=user)
        db.session.add(watchlist)
        db.session.commit()

@pytest.fixture()
def new_auction(app):
    with app.app_context():
        stmt = db.select(User).filter_by(id=1)
        user = db.session.scalar(stmt)
        auction = Auction(title="test auction", description="test auction description", status="test status", user=user, current_price=100)
        db.session.add(auction)
        db.session.commit()
    return auction

@pytest.fixture()
def new_bid(app):
    with app.app_context():
        stmt = db.select(User).filter_by(id=1)
        user = db.session.scalar(stmt)
        stmt = db.select(Auction).filter_by(id=1)
        auction = db.session.scalar(stmt)
        db.session.add(auction)
        bid = Bid(amount=100, auction=auction, user=user)
        db.session.add(bid)
        db.session.commit()
    return bid