"""This module contains the data store

and data logic of the store's products
"""
from .. import database

class Products():
    def __init__(self, product_id=None, product_name=None, product_price=None, category=None):
        self.product_name = product_name
        self.product_price = product_price
        self.category = category
        self.product_id = product_id


    def save(self):
        query = """
        INSERT INTO products(product_name, product_price, category) VALUES(
            '{}', '{}', '{}'
        )""".format(self.product_name, self.product_price, self.category)

        database.insert_to_db(query)

    def fetch_product_by_name(self):
        """Queries db for a product

        based on it's product name
        """
        # Query db for user with those params
        query = """
        SELECT * FROM products
        WHERE product_name = '{}'""".format(self.product_name)

        return database.select_from_db(query)

    def fetch_all_products(self):
        """Fetches all products from

        the database
        """
        query = """SELECT * FROM products"""
        return database.select_from_db(query)

    def put(self):
        query = """UPDATE products SET product_name = '{}', product_price = '{}',
        category = '{}' WHERE product_id = {}""".format(self.product_name, self.product_price,
                                                        self.category, self.product_id)

        database.insert_to_db(query)

    def delete(self):
        query = """DELETE FROM products WHERE product_id = {}""".format(self.product_id)
        database.insert_to_db(query)