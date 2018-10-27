"""Module contains tests for admin

specific endpoints
"""

import json

from flask import current_app

from app.api.v2 import database
from . import base_test
from . import common_functions

class TestProduct(base_test.TestBaseClass):
    """ Class contains tests for admin specific endpoints """

    def test_add_new_product(self):
        """Test POST /products"""
        self.register_test_admin_account()
        token = self.login_test_admin()

        # send a dummy data response for testing
        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['product']['product_name'], self.PRODUCT['product_name'])
        self.assertEqual(common_functions.convert_response_to_json(
            response)['product']['product_price'], self.PRODUCT['product_price'])
        self.assertEqual(common_functions.convert_response_to_json(
            response)['product']['category'], self.PRODUCT['category'])
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Product added successfully')

    def test_add_new_product_parameter_missing(self):
        """Test POST /products

        with one of the required parameters missing
        """
        self.register_test_admin_account()
        token = self.login_test_admin()

        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json={'product_name': 'Nyundo'}, headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Request missing a required argument')

    def test_add_new_product_price_under_one(self):
        """Test POST /products

        with the price of the product below minimum
        """
        self.register_test_admin_account()
        token = self.login_test_admin()

        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json={
                'product_id': 1, 'product_name': "Hammer", 'product_price': 0, 'category':'Tools'
                }, headers=dict(Authorization=token),
                content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'],
            'Price of the product should be a positive integer above 0.')


    def test_add_new_product_with_product_name_not_string(self):
        """Test POST /products

        with the product name not a string
        """
        self.register_test_admin_account()
        token = self.login_test_admin()

        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json={
                'product_id': 1, 'product_name': 200, 'product_price': 200, 'category':'Tools'
                }, headers=dict(Authorization=token),
                content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'],
            'Product name should be a string')

    def test_add_new_product_with_category_not_string(self):
        """Test POST /products

        with the category not a string
        """
        self.register_test_admin_account()
        token = self.login_test_admin()

        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json={
                'product_id': 1, 'product_name': "Hammer", 'product_price': 200, 'category': 200
                }, headers=dict(Authorization=token),
                content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'],
            'Bad request. The Category should be a string')

    def test_add_new_product_with_product_name_already_existing(self):
        """Test POST /products

        with the product name already existing
        """
        self.register_test_admin_account()
        token = self.login_test_admin()

        self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json={
                'product_id': 1, 'product_name': "Hammer", 'product_price': 200, 'category': "Tools"
                }, headers=dict(Authorization=token),
                content_type='application/json')

        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json={
                'product_id': 1, 'product_name': "Hammer", 'product_price': 200, 'category': "Tools"
                }, headers=dict(Authorization=token),
                content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'],
            'Record already exists in the database')

    def test_retrieve_all_products(self):
        """Test GET /products - when products exist"""
        self.register_test_admin_account()
        token = self.login_test_admin()

        # send a dummy data response for testing
        self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=token),
            content_type='application/json')


        response = self.app_test_client.get(
            '{}/products'.format(self.BASE_URL),
            headers=dict(Authorization=token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['products'][0][1], self.PRODUCT['product_name'])

    def test_retrieve_specific_product(self):
        """Test GET /products/id - when product exist"""

        self.register_test_admin_account()
        token = self.login_test_admin()

        # send a dummy data response for testing
        insert_query = """INSERT INTO products (product_name, product_price, category)
        VALUES ('Phone Model 1', 50000, 'Phones')
        """
        database.insert_to_db(insert_query)

        query = """SELECT * FROM products where product_name = 'Phone Model 1'"""
        product_id = database.select_from_db(query)
        response = self.app_test_client.get(
            '{}/product/{}'.format(self.BASE_URL, product_id[0][0]),
            headers=dict(Authorization=token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['product'][0][1], self.PRODUCT['product_name'])