"""This module contains the data store

and data logic of the store attendant's sale orders
"""
import datetime
from flask import jsonify

from .. import database

class SaleOrder():
    def __init__(self, product_name=None, product_price=None, quantity=None):
        self.product_name = product_name
        self.product_price = product_price
        self.quantity = quantity
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self):
        amount = (self.quantity * self.product_price)

        query = """
        INSERT INTO saleorders(product_name, product_price, quantity, amount, date_ordered) VALUES(
            '{}', '{}', '{}', '{}', '{}'
        )""".format(self.product_name, self.product_price, self.quantity, amount, self.date)

        database.insert_to_db(query)

    def get(self):
        """
            Queries db for user with given username
            Returns user object
        """
        # Query db for user with those params
        query = """
        SELECT * FROM saleorders"""

        return database.select_from_db(query)