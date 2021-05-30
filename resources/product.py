from flask import Flask, request
from flask_restful import Resource
from flask_jwt import jwt_required
from models.user import UserModel
from sqlalchemy.sql import func
from models.product import ProductModel
from db import db

class Product(Resource):
    #@jwt_required
    def post(self, name):
        user = UserModel.get_user_role(UserModel.user_name)
        if user.role == 'A':
            data = request.get_json()
        else:
            return {'message': 'only admin is authorized to add a product'}
        
        productId = ProductModel.get_product_id()
        
        product = ProductModel(productId['productid'], name, data['price'])
        product.save_to_db()
        return {'message': 'product added successfully'}

    #@jwt_required
    def delete(self,name):
        user = UserModel.get_user_role(UserModel.user_name)
        if user.role == 'A':
            data = request.get_json()
        else:
            return {'message': 'only admin is authorized to delete a product'}

        product = ProductModel.get_product_by_name(name)
        product.delete_from_db()
        return{'message': 'Product deleted sucessfully'}

    #@jwt_required
    def put(self, name):
        user = UserModel.get_user_role(UserModel.user_name)
        if user.role == 'A':
            data = request.get_json()
        else:
            return {'message': 'only admin is authorized to delete a product'}

        product = ProductModel.get_product_by_name(name)
        
        if product:
            product.price = data['price']
            product.save_to_db()
            return {'message': 'price of ' + name + ' updated successfully'}
        else:
           productId = ProductModel.get_product_id()
           product = ProductModel(productId['productid'], name, data['price'])
           product.save_to_db()
           return {'message': 'product ' + name + ' added successfully'}

    #@jwt_required
    def get(self, name):
        search = "%{}%".format(name)
        product_list = ProductModel.get_product_by_partial_name(search)
        
        if product_list:
            return {'product': [each_product.json() for each_product in product_list]}
        
        return {'message': 'search string does not match any product'}

    
class ProductList(Resource):
    def get(self):
        product_list = ProductModel.get_all_products()
        return {'product': [each_product.json() for each_product in product_list]}

