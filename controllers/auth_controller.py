from flask import Blueprint, request, render_template
from models.user import User, user_schema
from init import bcrypt, db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register")
def register_user_get():
    return render_template("register.html")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        body = request.form

        user = User(
            email = body.get("email"),
            username = body.get("username"),
        )

        password = body.get("password")
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # Add the user to the database
        db.session.add(user)
        # Commit the changes to the database
        db.session.commit()

        return render_template('login.html')
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"Error": f"Missing required field: {err.orig.diag.column_name}"}, 400
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"Error": f"Field not unique"}, 400

@auth_bp.route("/login")
def login_user_get():
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login_user():
    body = request.form
    email = body.get('email')
    # body = request.get_json()
    # Execute the SQL query to fetch the user with the same email as login data
    stmt = db.select(User).filter_by(email=email)
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, body.get("password")):
        token = create_access_token(identity=str(user.id),expires_delta=timedelta(days=1))
        return {"email": user.email, "username": user.username, "token": token}
    else:
        return render_template("login.html", message="Username and/or password not correct!")