from flask import Blueprint, request
from models.user import User, user_schema
from init import bcrypt, db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    body = request.get_json()

    user = User(
        email = body.get("email"),
        username = body.get("username"),
    )

    password = body.get("password")
    if password:
        user.password = bcrypt.generate_password_hash(password).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    return user_schema.dump(user), 200

@auth_bp.route("/login")
def login_user():
    pass