import sqlite3
from db import db
from sqlalchemy.sql import func

class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(6))
    name = db.Column(db.String(30))
    price = db.Column(db.Float(precision=2))
    
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    @classmethod
    def get_product_id(cls):
        productId = 'P00001'
        product = db.session.query(func.max(ProductModel.product_id)).scalar()
        if product:
            ProdIdMax = product
            ProdIdMax5 = int(ProdIdMax[1:6]) + 1
            productId = ProdIdMax[0:1] + f'{ProdIdMax5:05d}'

        return {'productid': productId}

    @classmethod
    def get_product_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return{'product_id': self.product_id,
               'name': self.name,
               'price': self.price
               }

    @classmethod
    def get_product_by_partial_name(cls, searchstr):
        return cls.query.filter(ProductModel.name.like(searchstr)).all()

    @classmethod
    def get_all_products(cls):
        return cls.query.all()

