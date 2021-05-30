import sqlite3
from db import db
        
class UserModel(db.Model):
    __tablename__ = 'users'
        
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(80))
    phone = db.Column(db.Integer)
    role = db.Column(db.String(1))

    #user_name is a global valiable. This is used to check user role
    user_name = ''  
    
    def __init__(self):
        self.id = userid
        self.username = username
        self.password = password
        self.role = role
        
    @classmethod
    def get_user_by_username(cls,username):
        UserModel.user_name = username
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_userid(cls, userid):
        return cls.query.filter_by(id=userid).first()

    @classmethod
    def get_user_role(cls, username):
        return cls.query.filter_by(username=username).first()
    
