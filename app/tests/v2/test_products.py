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
        # send a dummy data response for testing
        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
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

    def test_add_new_product_inventory_missing(self):
        """Test POST /products

        with one of the required parameters missing
        """
        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json={
                'product_name': 'Nyundo'
                }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Indicate the amount of stock present')

    def test_add_new_product_price_under_one(self):
        """Test POST /products

        with the price of the product below minimum
        """
        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json={
                'product_name': "Hammer", 'product_price': 0,
                'category': self.category_id, 'inventory': 10, 'min_quantity': 5
                }, headers=dict(Authorization=self.token),
                content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'],
            'Price of the product should be a positive integer above 0.')

    def test_add_new_product_price_not_integer(self):
        """Test POST /products

        with the price of the product below minimum
        """
        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json={
                'product_name': "Hammer", 'product_price': "string",
                'category':self.category_id, 'inventory': 10, 'min_quantity': 5
                }, headers=dict(Authorization=self.token),
                content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'],
            'Product price should be an integer')

    def test_add_new_product_with_product_name_not_string(self):
        """Test POST /products

        with the product name not a string
        """
        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json={
                'product_name': 300, 'product_price': 300,
                'category':self.category_id, 'inventory': 10, 'min_quantity': 5
                }, headers=dict(Authorization=self.token),
                content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'],
            'Product name should be a string')

    def test_add_new_product_with_category_not_recognized(self):
        """Test POST /products

        with the category not a string
        """
        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json={
                'product_name': "Hammer", 'product_price': 300,
                'category': -1, 'inventory': 10, 'min_quantity': 5
                }, headers=dict(Authorization=self.token),
                content_type='application/json')

        self.assertEqual(response.status_code, 406)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'],
            'Please add a recognized category. -1 is not.')

    def test_add_new_product_with_product_name_already_existing(self):
        """Test POST /products

        with the product name already existing
        """
        self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
                content_type='application/json')

        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
                content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'],
            'Record already exists in the database')

    def test_retrieve_all_products(self):
        """Test GET /products - when products exist"""
        # send a dummy data response for testing
        self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
            content_type='application/json')

        response = self.app_test_client.get(
            '{}/products'.format(self.BASE_URL),
            headers=dict(Authorization=self.token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['products'][0]['product_name'], self.PRODUCT['product_name'])

    def test_retrieve_all_products_none_found(self):
        """Test GET /products - when products exist"""
        response = self.app_test_client.get(
            '{}/products'.format(self.BASE_URL),
            headers=dict(Authorization=self.token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "There are no products in the store yet")

    def test_retrieve_specific_product(self):
        """Test GET /products/id - when product exist"""
        # send a dummy data response for testing
        insert_query = """INSERT INTO products (product_name, product_price, category, inventory, min_quantity, added_by)
        VALUES ('Hammer', 50000, {}, 12, 4, 1)
        """.format(self.category_id)
        database.insert_to_db(insert_query)

        query = """SELECT * FROM products where product_name = 'Hammer'"""
        product_id = database.select_from_db(query)
        response = self.app_test_client.get(
            '{}/product/{}'.format(self.BASE_URL, product_id[0]['product_id']),
            headers=dict(Authorization=self.token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['product'][0]['product_name'], 'Hammer')

    def test_retrieve_specific_product_not_found(self):
        """Test GET /products/id - when product exist"""
        response = self.app_test_client.get(
            '{}/product/1000'.format(self.BASE_URL),
            headers=dict(Authorization=self.token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 404)

    def test_update_product(self):
        """PUT /product/id - with expected success"""
        self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
            content_type='application/json')

        query = """SELECT product_id FROM products WHERE product_name = 'Phone Model 1'"""
        product_id = database.select_from_db(query)

        response = self.app_test_client.put('{}/product/{}'.format(
            self.BASE_URL, product_id[0]['product_id']),
             json={
                 'product_price': 400,
                 'category': self.category_id,
                 'inventory': 5,
                 'min_quantity': 3,
             },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        #self.assertEqual(response.status_code, 202)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "Product updated successfully")

    def test_update_product_missing_parameter(self):
        """PUT /product/id - with expected success"""
        self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
            content_type='application/json')

        query = """SELECT product_id FROM products WHERE product_name = 'Phone Model 1'"""
        product_id = database.select_from_db(query)

        response = self.app_test_client.put('{}/product/{}'.format(
            self.BASE_URL, product_id[0]['product_id']),
             json={
                 'product_name':'Jembe',
                 'product_price': 300
             },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 403)


    def test_delete_product(self):
        """DELETE /product/id"""
        self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
            content_type='application/json')

        query = """SELECT product_id FROM products WHERE product_name = 'Phone Model 1'"""
        product_id = database.select_from_db(query)

        response = self.app_test_client.delete('{}/product/{}'.format(
            self.BASE_URL, product_id[0]['product_id']),
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "Product deleted successfully")


    def test_non_json_data(self):
        """Test POST /products"""
        # send a dummy data response for testing
        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
            content_type='application/text')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Request data must be in json format')