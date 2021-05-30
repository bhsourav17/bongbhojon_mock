import sqlite3
from flask_restful import Resource
from flask import request
from models.user import UserModel

class UserRegister(Resource):
    def post(self):
        login_data = request.get_json()

        if UserModel.get_user_by_username(login_data['username']):
            return {'message': 'A user with username ' + login_data['username'] + ' already exists'}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        #role should always be 'U' as only user will register him/herself
        query = "INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (login_data['username'], login_data['password'], login_data['firstname'], login_data['lastname'], login_data['address'],  \
                       login_data['phone'], 'U'))

        connection.commit()
        connection.close()

        return{'message': 'user added successfully'}


        
