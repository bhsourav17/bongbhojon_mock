import sqlite3
from db import db
import shortuuid
from sqlalchemy.sql import func

class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(22))
    order_no = db.Column(db.Integer)
    username = db.Column(db.String(30))
    order_date = db.Column(db.String(8))
    delivery_date = db.Column(db.String(8))
    product_id = db.Column(db.String(6))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float(precision=2))
    
    def __init__(self, order_id, order_no, username, order_date, delivery_date, product_id, quantity, price):
        self.order_id = order_id
        self.order_no = order_no
        self.username = username
        self.order_date = order_date
        self.delivery_date = delivery_date
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    @classmethod
    def get_order_id(cls):
        return{'orderid': shortuuid.uuid()}

    @classmethod
    def get_order_no(cls):
        orderNo = 100001
        order = db.session.query(func.max(OrderModel.order_no)).scalar()
        if order:
            orderNo = order + 1

        return {'orderno': orderNo} 

    def json(self):
        return{'order_id': self.order_id,
               'order_no': self.order_no,
               'username': self.username,
               'order_date': self.order_date,
               'delivery_date': self.delivery_date,
               'product_id': self.product_id,
               'quantity': self.quantity,
               'price': self.price
               }

    @classmethod
    def get_order_for_user_within_date(cls, user_name, delivery_start_date, delivery_end_date):
        return cls.query.filter(OrderModel.username==user_name, OrderModel.delivery_date >= delivery_start_date, OrderModel.delivery_date <= delivery_end_date).all()

    @classmethod
    def get_order_for_admin_within_date(cls, delivery_start_date, delivery_end_date):
        return cls.query.filter(OrderModel.delivery_date >= delivery_start_date, OrderModel.delivery_date <= delivery_end_date).all()

    @classmethod
    def get_all_orders_for_user(cls, user_name):
        return cls.query.filter(OrderModel.username==user_name).all()

    @classmethod
    def get_all_orders_for_admin(cls):
        return cls.query.filter().all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    
