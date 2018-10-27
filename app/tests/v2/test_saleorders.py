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
        self.register_test_admin_account()
        token = self.login_test_admin() 

        # send a dummy data response for testing
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json=self.SALE_ORDERS, headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['saleorder']['product_name'], self.SALE_ORDERS['product_name'])
        self.assertEqual(common_functions.convert_response_to_json(
            response)['saleorder']['product_price'], self.SALE_ORDERS['product_price'])
        self.assertEqual(common_functions.convert_response_to_json(
            response)['saleorder']['quantity'], self.SALE_ORDERS['quantity'])
        self.assertEqual(common_functions.convert_response_to_json(
            response)['saleorder']['amount'], self.SALE_ORDERS['amount'])
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Checkout complete')


    def test_create_sale_order_parameter_missing(self):
        """Test POST /saleorder

        with one of the required parameters missing
        """
        self.register_test_admin_account()
        token = self.login_test_admin()

        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={'product_name': 'Nyundo'}, headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Request missing a required argument')


    def test_create_sale_order_price_below_one(self):
        """Test POST /saleorder

        with the price not a valid integer
        """
        self.register_test_admin_account()
        token = self.login_test_admin()

        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={'product_name': 'Nyundo', 'product_price': -1, 'quantity': 1},
            headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Bad request. Price of the product should be a positive integer above 0.')


    def test_create_sale_order_invalid_product_name(self):
        """Test POST /saleorder

        with the product name not a string
        """
        self.register_test_admin_account()
        token = self.login_test_admin()

        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={'product_name': 3, 'product_price': 300, 'quantity': 1},
            headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Bad request. Product name should be a string')


    def test_create_sale_order_price_not_digits(self):
        """Test POST /saleorder

        with the price not a valid integer
        """

        self.register_test_admin_account()
        token = self.login_test_admin()

        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={'product_name': "Nyundo", 'product_price': "300", 'quantity': 1},
            headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Bad request. The product price should be digits')


    def test_create_sale_order_invalid_quantity(self):
        """Test POST /saleorder

        with the quantity not a valid integer
        """
        self.register_test_admin_account()
        token = self.login_test_admin()
        
        response = self.app_test_client.post('{}/saleorder'.format(
            self.BASE_URL), json={'product_name': "Nyundo", 'product_price': 300, 'quantity': "1"}, 
            headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], 'Bad request. The quantity should be specified in digits')


    def test_retrieve_specific_sale_order(self):
        """Test GET /saleorder/id - when saleorder exists"""

        self.register_test_admin_account()
        token = self.login_test_admin()

        self.app_test_client.post(
        '{}/saleorder'.format(self.BASE_URL), json={
            'product_name': "Test Product",
            'product_price': 20,
            'quantity': 1,
            'amount': 20
        },
        headers=dict(Authorization=token),
        content_type='application/json')

        query = """SELECT saleorder_id FROM saleorders WHERE product_name = 'Test Product'"""
        saleorder_id = database.select_from_db(query)
        print(saleorder_id[0][0])
        response = self.app_test_client.get(
            '{}/saleorder/{}'.format(self.BASE_URL, saleorder_id[0][0]),
            headers=dict(Authorization=token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 200)


    def test_fetch_sale_orders(self):
        """Test GET /saleorder - when sale order exists"""
        self.register_test_admin_account()
        token = self.login_test_admin()

        self.app_test_client.post(
        '{}/saleorder'.format(self.BASE_URL), json={
            'product_name': "Test Product",
            'product_price': 20,
            'quantity': 1,
            'amount': 20
        },
        headers=dict(Authorization=token),
        content_type='application/json')
                                                                
        response = self.app_test_client.get(
            '{}/saleorder'.format(self.BASE_URL),

            headers=dict(Authorization=token),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['sale_orders'][0][2], "Test Product")
        self.assertEqual(common_functions.convert_response_to_json(
           response)['sale_orders'][0][3], 20)