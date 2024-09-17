from init import db, ma


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.string, nullable=False, unique=True)
    password = db.Column(db.string, nullable=False)
    role = db.Column(db.string, nullable=False)
    watchlist = db.column(db.Integer)

    class UserSchema(ma.Schema):
        class Meta:
            fields = ("id", "username", "password", "role", "watchlist")
    
    user_schema = UserSchema(exclude=["password"])
    users_schema = UserSchema(many=True, exclude=["password"])