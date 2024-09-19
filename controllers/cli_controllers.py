from flask import Blueprint
from init import db, bcrypt
from models.user import User

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

    db.session.commit()
    
    print("Users created")


@db_commands.cli.command("drop")
def delete_tables():
    db.drop_all()
    print("Tables dropped!")