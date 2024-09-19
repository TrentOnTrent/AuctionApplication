from flask import Blueprint, request
from models.user import User, user_schema
from init import bcrypt, db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token
from datetime import timedelta

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
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"Error": f"Missing required field: {err.orig.diag.column_name}"}, 400
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"Error": f"Field not unique"}, 400

@auth_bp.route("/login", methods=["POST"])
def login_user():
    body = request.get_json()
    stmt = db.select(User).filter_by(email=body.get("email"))
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, body.get("password")):
        token = create_access_token(identity=str(user.id),expires_delta=timedelta(days=1))
        return {"email": user.email, "username": user.username, "token": token}
    else:
        return {"error": "Invalid email or password"}, 400