"""This module contains the data store

and data logic of the store's products category
"""
from .. import database

class Category():
    def __init__(self, category_id=None, category_name=None):
        self.category_name = category_name
        self.category_id = category_id


    def save(self):
        query = """
        INSERT INTO category(category_name) VALUES(
        '{}')""".format(self.category_name)
        

        database.insert_to_db(query)

    def get(self):
        """Fetches all categories from

        the database
        """
        query = """SELECT * FROM category"""
        return database.select_from_db(query)

    def put(self):
        query = """UPDATE category SET category_name = '{}' 
        WHERE category_id = {}""".format(self.category_name, self.category_id)

        database.insert_to_db(query)

    def delete(self):
        query = """DELETE FROM category WHERE category_id = {}""".format(self.category_id)
        database.insert_to_db(query)