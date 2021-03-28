from models.user import UserModel #because user.py and security.py are in same folder, we import User class from user.py file
from werkzeug.security import safe_str_cmp #because of string comparing issues in some python versions

def authenticate(username, password):
    user = UserModel.find_by_username(username) #get the user which has the username provided to the function, if not found return None
    if user and safe_str_cmp(user.password, password): #check if user exists and his password is matching our database
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
