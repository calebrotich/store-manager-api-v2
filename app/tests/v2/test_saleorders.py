"""Module contains tests to endpoints that 

are general to both the admin and the normal user
"""

import json

from app.api.v2 import database
from . import base_test
from . import common_functions

class TestSaleOrder(base_test.TestBaseClass):
    """Class contains the general user, i.e. both admin

    and normal user, endpoints' tests
    """
    def test_create_sale_order(self):
        """Test POST /saleorder"""
        response = self.app_test_client.post('{}/products'.format(
        self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
        content_type='application/json')

        # send a dummy data response for testing
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json=self.SALE_ORDERS, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Checkout complete')


    def test_create_sale_order_quantity_missing(self):
        """Test POST /saleorder

        with the quantity parameter is missing
        """
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={
                'items': [{
                    'product': 1
                }]
            }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Kindly specify the quantity of the product you want')


    def test_create_sale_order_invalid_product_value(self):
        """Test POST /saleorder

        with the product name not a string
        """
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={
                'items': [{
                    'product': 'Phone Model 1',
                    'quantity': 3
                }]
            },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Please select the a product you want to purchase')


    def test_create_sale_order_items_not_in_list(self):
        """Test POST /saleorder

        with the product name not a string
        """
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={
                'items': {
                    'product': 1,
                    'quantity': 3
                }
            },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'The value should be a list of dictionaries')

    def test_create_sale_order_items_key_missing(self):
        """Test POST /saleorder

        with the product name not a string
        """
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={},
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'list of items missing')

    def test_create_sale_order_quantity_not_digits(self):
        """Test POST /saleorder

        with the price not a valid integer
        """
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={
                'items': [{
                    'product': 1,
                    'quantity': 'string'
                }]
            },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
        response)['message'], 'Please have a number for the quantity value')

    def test_create_sale_order_missing_product_parameter(self):
        """Test POST /saleorder

        with the product parameter missing
        """
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={
                'items': [{
                    'quantity': 4
                }]
            },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(common_functions.convert_response_to_json(
        response)['message'], 'Kindly specify the product you want to buy')

    def test_create_sale_order_quatity_greater_than_inventory(self):
        """Test POST /saleorder"""
        response = self.app_test_client.post('{}/products'.format(
        self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
        content_type='application/json')

        # send a dummy data response for testing
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={
                'items': [
                    {
                        'product': 1,
                        'quantity': 52
                    }
                ]
            }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "Our current stock cannot serve an order of 52. You can currently order a maximum of 50 for the product 'Phone Model 1'")

    def test_create_sale_order_quatity_less_than_one(self):
        """Test POST /saleorder"""
        response = self.app_test_client.post('{}/products'.format(
        self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
        content_type='application/json')

        # send a dummy data response for testing
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={
                'items': [
                    {
                        'product': 1,
                        'quantity': 0
                    }
                ]
            }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "Please have a quantity value over 0")

    def test_create_sale_order_inventory_equal_to_zero(self):
        """Test POST /saleorder"""
        response = self.app_test_client.post('{}/products'.format(
        self.BASE_URL), json={
            'product_name': 'Phone Model 1',
            'product_price': 55000,
            'min_quantity': 10,
            'inventory': 0,
            'category': self.category_id
        }, headers=dict(Authorization=self.token),
        content_type='application/json')

        # send a dummy data response for testing
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={
                'items': [
                    {
                        'product': 1,
                        'quantity': 52
                    }
                ]
            }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "Please eliminate Phone Model 1 from your sale. It is currently out of stock")


    def test_create_saleorder_product_missing(self):
        """Test POST /saleorder"""
        # send a dummy data response for testing
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={
                'items': [
                    {
                        'product': -1,
                        'quantity': 52
                    }
                ]
            }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "Product with id -1 is not available in the store")

    def test_retrieve_specific_sale_order(self):
        """Test GET /saleorder/id - when saleorder exists"""
        self.app_test_client.post('{}/products'.format(
        self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
        content_type='application/json')

        self.app_test_client.post(
        '{}/saleorder'.format(self.BASE_URL), json=self.SALE_ORDERS,
        headers=dict(Authorization=self.token),
        content_type='application/json')

        response = self.app_test_client.get(
            '{}/saleorder/1'.format(self.BASE_URL),
            headers=dict(Authorization=self.token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
        response)['message'], 'Sale order fetched successfully')

    def test_retrieve_specific_sale_order_not_found(self):
        """Test GET /saleorder/id - when saleorder exists"""
        response = self.app_test_client.get(
            '{}/saleorder/100'.format(self.BASE_URL),
            headers=dict(Authorization=self.token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(common_functions.convert_response_to_json(
        response)['message'], 'Sale Order with id 100 not found')
        

    def test_fetch_sale_orders(self):
        """Test GET /saleorder - when sale order exists"""
        self.app_test_client.post('{}/products'.format(
        self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=self.token),
        content_type='application/json')

        self.app_test_client.post(
        '{}/saleorder'.format(self.BASE_URL), json=self.SALE_ORDERS,
        headers=dict(Authorization=self.token),
        content_type='application/json')
                                                                
        response = self.app_test_client.get(
            '{}/saleorder'.format(self.BASE_URL),
            headers=dict(Authorization=self.token),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['sale_orders'][0]['amount'], 110000)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "Successfully fetched all the sale orders")


    def test_fetch_sale_orders_no_data(self):
        """Test GET /saleorder - when sale order exists"""
        response = self.app_test_client.get(
            '{}/saleorder'.format(self.BASE_URL),
            headers=dict(Authorization=self.token),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "No sale orders created yet")