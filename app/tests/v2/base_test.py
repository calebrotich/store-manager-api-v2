"""
    Contains the base test class for the
    other test classes
"""
import unittest
import os

# local imports
from app import create_app
from instance.config import config
from . import common_functions
from ...api.v2.database import init_db, drop_table_if_exists
from app.api.v2 import database


class TestBaseClass(unittest.TestCase):
    """Base test class"""


    def setUp(self):
        """Create and setup the application

        for testing purposes
        """
        self.app = create_app(os.getenv('FLASK_ENV'))
        self.BASE_URL = 'api/v2'
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app_test_client = self.app.test_client()
        self.app.testing = True

        with self.app.app_context():
            self.db_url = config['test_db_url']
            init_db(self.db_url)

        self.PRODUCT = {
        'product_name': 'Phone Model 1',
        'product_price': 55000,
        'min_quantity': 10,
        'inventory': 50,
        'added_by': 'user@gmail.com',
        'category': self.create_product_category()
        }

        self.SALE_ORDERS = {
        'items': [
            {
                'product_name': 'Phone Model 1',
                'quantity': 2
            }
        ]
        }


    def tearDown(self):
        """Destroy the application that

        is created for testing
        """
        with self.app.app_context():
            init_db(self.db_url)
        self.app_context.pop()

    def create_product_category(self):
        query = """INSERT INTO category (category_name) VALUES ('Tools')"""
        database.insert_to_db(query)

        fetch_query = """SELECT * FROM category WHERE category_name = 'Tools'"""
        category_name = database.select_from_db(fetch_query)

        return category_name[0]['category_name']

    def register_test_admin_account(self):
        #Register admin
        """Registers an admin test user account"""
            
        res = self.app_test_client.post("api/v2/auth/signup/admin",
        json={
        "email": "user@gmail.com",
        "role": "admin",
        "password": "Password12#"
        }, 
        headers={
        "Content-Type": "application/json"
        })

        return res

    def register_test_attendant_account(self):
        #Register attendant
        """Registers an attendant test user account"""
        token = self.login_test_admin()
        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "attendant@gmail.com",
        "role": "attendant",
        "password": "Password12#"
        }, 
        headers=dict(Authorization=token),
        content_type='application/json'
        )

        return res
    
    def login_test_admin(self):
        """Validates the test account for the admin"""
        self.register_test_admin_account()
        
        # Login the test account for the admin
        resp = self.app_test_client.post("api/v2/auth/login",
        json={
            "email": "user@gmail.com",
            "password": "Password12#"
        },
        headers={
        "Content-Type": "application/json"
        })

        auth_token = common_functions.convert_response_to_json(
        resp)['token']

        return auth_token

    def login_test_attendant(self):
        """Validates the test account for the attendant"""

        # Login the test account for the admin
        resp = self.app_test_client.post("api/v2/auth/login",
        json={
            "email": "attendant@gmail.com",
            "password": "Password12#"
        },
        headers={
        "Content-Type": "application/json"
        })

        auth_token = common_functions.convert_response_to_json(
        resp)['token']

        return auth_token

if __name__ == '__main__':
    unittest.main()