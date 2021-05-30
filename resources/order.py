import sqlite3, datetime
from flask_restful import Resource
from flask import Flask, request
from models.order import OrderModel
from flask_jwt import jwt_required
from models.user import UserModel
from models.product import ProductModel


class Order(Resource):
    #@jwt_required
    def post(self, name):
        user = UserModel.get_user_role(UserModel.user_name)
        if user.role == 'U':
            data = request.get_json()
        else:
            return {'message': 'Only user is authorized to place an order. Admin cannot place.'}

        #get order_id from shortuuid
        order_id = OrderModel.get_order_id() #value is in order_id['orderid']

        #get order_no. it starts from 100001 and increases by one for each new order
        order_no = OrderModel.get_order_no() #value is in order_no['orderno']

        #populate username
        username = UserModel.user_name

        #populate current date as order date
        curr_date = datetime.datetime.now()
        order_date = str(curr_date.strftime("%Y%m%d"))
        
        #populate delivery date from input
        delivery_date = str(data['delivery_date'])

        #get product_id using product name
        product = ProductModel.get_product_by_name(name) # value is in product.product_id
        product_id = product.product_id

        #populate quantity from input
        quantity = int(data['quantity'])

        #calculate price
        price = data['quantity'] * product.price

        order = OrderModel(order_id['orderid'], order_no['orderno'], username, order_date, delivery_date, product_id, quantity, price)
        order.save_to_db()
        return {'message': 'order placed successfully'}

class OrderList(Resource):
    #@jwt_required
    def delete(self):
        user = UserModel.get_user_role(UserModel.user_name)

        delivery_start_date = 99991231
        
        if user.role == 'U':
            try:
                data = request.get_json()
                delivery_start_date = data['delivery_start_date']
            except:
                pass
        else:
            return {'message': 'Only user is authorized to delete an order. Admin cannot delete.'}

        if delivery_start_date != 99991231:
            delivery_start_date = data['delivery_start_date']
            delivery_end_date = data['delivery_end_date']
            order_list = OrderModel.get_order_for_user_within_date(UserModel.user_name, delivery_start_date, delivery_end_date)
            if order_list:
                for each_order in order_list:
                    each_order.delete_from_db()
                return {'message': 'Orders of username: ' + UserModel.user_name + ' from ' + str(delivery_start_date) + ' to ' + str(delivery_end_date) + ' deleted successfully'}
            else:
                return {'message': 'No order found for username: ' + UserModel.user_name + ' for given dates'}
        else:
            order_list = OrderModel.get_all_orders_for_user(UserModel.user_name)
            if order_list:
                for each_order in order_list:
                    each_order.delete_from_db()
                return {'message': 'All orders of username: ' + UserModel.user_name + ' deleted successfully'}
            else:
                return {'message': 'No order found for username: ' + UserModel.user_name}
            
    #@jwt_required
    def get(self):
        user = UserModel.get_user_role(UserModel.user_name)

        delivery_start_date = 99991231
        
        try:
            data = request.get_json()
            delivery_start_date = data['delivery_start_date']
        except:
            pass

        if delivery_start_date != 99991231:
            delivery_start_date = data['delivery_start_date']
            delivery_end_date = data['delivery_end_date']
            
            if user.role == 'A':
                order_list = OrderModel.get_order_for_admin_within_date(delivery_start_date, delivery_end_date)
            else:
                order_list = OrderModel.get_order_for_user_within_date(UserModel.user_name, delivery_start_date, delivery_end_date)
        else:
            if user.role == 'A':
                order_list = OrderModel.get_all_orders_for_admin()
            else:
                order_list = OrderModel.get_all_orders_for_user(UserModel.user_name)

        return {'order': [each_order.json()for each_order in order_list]}
    
