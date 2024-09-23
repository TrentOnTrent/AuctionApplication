import pytest
import os
from main import create_app
from init import db, ma, bcrypt, jwt
from models.user import User
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

@pytest.fixture(scope='module')
def new_user():
    user = User(email="unittest@test.com", username="unittest", password="unittestpassword")
    return user