"""This module contains the data store

and data logic of the store's products
"""
from .. import database

class Products():
    def __init__(self, product_id=None, product_name=None, product_price=None,
     category=None, min_quantity=None, inventory=None, added_by=None):
        self.product_name = product_name
        self.product_price = product_price
        self.category = category
        self.product_id = product_id
        self.min_quantity = min_quantity
        self.inventory = inventory
        self.added_by = added_by


    def save(self):
        query = """INSERT INTO products(product_name, product_price, category, min_quantity, inventory, added_by)
        VALUES('{}', {}, '{}',{},{}, '{}')""".format(self.product_name, self.product_price,
        self.category, self.min_quantity, self.inventory, self.added_by)

        database.insert_to_db(query)

    def fetch_all_products(self):
        """Fetches all products from

        the database
        """
        query = """SELECT * FROM products"""
        return database.select_from_db(query)

    def put(self):
        query = """UPDATE products SET product_price = {},
        category = '{}', inventory={}, min_quantity={} WHERE product_id = {}""".format(self.product_price,
                                                        self.category, self.inventory, self.min_quantity, self.product_id)

        database.insert_to_db(query)

    def delete(self):
        query = """DELETE FROM products WHERE product_id = {}""".format(self.product_id)
        database.insert_to_db(query)

    def deduct_inventory(self):
        query = """UPDATE products SET inventory = {} WHERE product_id = {}""".format(self.inventory, self.product_id)
        database.insert_to_db(query)