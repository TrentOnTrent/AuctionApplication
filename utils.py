from flask_jwt_extended import get_jwt_identity

import functools

from init import db
from models.user import User

def auth_as_admin_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # get the user's id from get_jwt_identity
        user_id = get_jwt_identity()
        # fetch the user from the db
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        # if user is admin
        if user.admin_role:
            # allow the decorator fn to execute
            return fn(*args, **kwargs)
        # else
        else:
            # return error
            return {"error": "Only admin can perform this action"}, 403
    
    return wrapper