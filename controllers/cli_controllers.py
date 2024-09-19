from flask import Blueprint
from init import db
from models import user, auction, bid

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("delete")
def delete_tables():
    db.drop_all()
    print("Tables dropped!")