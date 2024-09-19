from flask import Blueprint, request
from models.user import User, user_schema
from init import bcrypt, db
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
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
    except IntegrityError:
        return {"Error": "Incorrect input"}, 400

@auth_bp.route("/login")
def login_user():
    body = request.get_json()

    