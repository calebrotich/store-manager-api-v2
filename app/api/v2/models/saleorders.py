"""This module contains the data store

and data logic of the store attendant's sale orders
"""
import datetime
from flask import jsonify

from .. import database

class SaleOrder():
    def __init__(self, saleorder_id=None, amount=None, made_by=None):
        self.amount = amount
        self.made_by = made_by
        self.saleorder_id = saleorder_id

    def save(self):
        query = """
        INSERT INTO saleorders(amount, made_by) VALUES(
            {}, '{}'
        )""".format(self.amount, self.made_by)

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

    def rollback_saleorder(self):
        query = """DELETE FROM saleorders WHERE saleorder_id = {}""".format(self.saleorder_id)
        database.insert_to_db(query)
    

class SaleItems():
    def __init__(self, saleorder_id=None, product=None, quantity=None):
        self.product = product
        self.saleorder_id = saleorder_id
        self.quantity = quantity

    def save(self):
        query = """
        INSERT INTO saleitems(saleorder_id, product, quantity) VALUES(
            {}, {}, {}
        )""".format(self.saleorder_id, self.product, self.quantity)

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
