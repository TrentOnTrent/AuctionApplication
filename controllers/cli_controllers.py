from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.auction import Auction
from models.bid import Bid

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("seed")
def seed_tables():
    users = [
        User(
            email = "admin@admin.com",
            username = "admin",
            password = bcrypt.generate_password_hash("admin").decode("utf-8"),
            admin_role = True
        ),
        User(
            email = "user1@auction.com",
            username = "User 1",
            password = bcrypt.generate_password_hash("password").decode("utf-8"),
            admin_role = False
        )
    ]
    db.session.add_all(users)
    auctions = [
        Auction(
            user = users[0],
            title = "Test Auction",
            description = "Description of Test Auction",
            status = "In Progress",
            current_price = "1.00",
        ), 
        Auction(
            user = users[0],
            title = "Test Auction 2",
            description = "Description of Test Auction 2",
            status = "In Progress",
            current_price = "5.50",
        ), 
        Auction(
            user = users[1],
            title = "Test Auction 3",
            description = "Description of Test Auction 3",
            status = "In Progress",
            current_price = "10.50",
        ), 
    ]
    db.session.add_all(auctions)

    bids = [
        Bid(
                auction = auctions[0],
                user = users[0],
                amount = 2
            ), 
            Bid(
                auction = auctions[0],
                user = users[0],
                amount = 3
            ), 
            Bid(
                auction = auctions[0],
                user = users[0],
                amount = 4
            )]
    db.session.add_all(bids)
    db.session.commit()
    
    print("Users and auctions created")


@db_commands.cli.command("drop")
def delete_tables():
    db.drop_all()
    print("Tables dropped!")