from models.user import UserModel

def authenticate(username, password):
    user = UserModel.get_user_by_username(username)

    if user and user.password == password:
        return user

def identity(payload):
    userid = payload['identity']
    return UserModel.get_user_by_userid(userid)


