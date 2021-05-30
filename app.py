from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.product import Product, ProductList
from resources.order import Order, OrderList
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACE_MODIFICATIONS'] = False

app.secret_key = "Welcome234"
api = Api(app)

jwt = JWT(app, authenticate, identity)

user_name = ''

api.add_resource(UserRegister,'/user/register')
api.add_resource(Product,'/product/<string:name>')
api.add_resource(ProductList,'/products')
api.add_resource(Order,'/order/<string:name>')
api.add_resource(OrderList,'/orders')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=1313, debug=True)
    
                 
