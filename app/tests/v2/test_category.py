"""Module defines test cases for product category"""

from . import base_test
from app.api.v2 import database
from . import common_functions


class TestCategory(base_test.TestBaseClass):
    """Class defines CRUD methods for product category"""


    def test_post_category(self):
        """POST /category"""

        self.register_test_admin_account()
        token = self.login_test_admin()

        response = self.app_test_client.post('{}/category'.format(
            self.BASE_URL), json=self.CATEGORY, headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(common_functions.convert_response_to_json(
            response)["message"], "Category created successfully")

    def test_post_category_missing_parameter(self):
        """POST /category"""

        self.register_test_admin_account()
        token = self.login_test_admin()

        response = self.app_test_client.post('{}/category'.format(
            self.BASE_URL), json={}, headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)["message"], "Request missing a required argument")


    def test_get_all_categories(self):
        self.register_test_admin_account()
        token = self.login_test_admin()
        query = """INSERT INTO category(category_name) VALUES('Tools')"""
        
        database.insert_to_db(query)
        response = self.app_test_client.get("{}/category".format(
            self.BASE_URL), headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
            response)["message"], "Categories fetched successfully")

    def test_get_all_categories_no_data(self):
        self.register_test_admin_account()
        token = self.login_test_admin()
        
        response = self.app_test_client.get("{}/category".format(
            self.BASE_URL), headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(common_functions.convert_response_to_json(
            response)["message"], "No categories created yet")

    def test_update_category(self):
        """PUT /product/id - with expected success"""

        self.register_test_admin_account()
        token = self.login_test_admin()

        query = """INSERT INTO category(category_name) VALUES('Tools')"""
        
        database.insert_to_db(query)

        query = """SELECT category_id FROM category WHERE category_name = 'Tools'"""
        category_id = database.select_from_db(query)

        response = self.app_test_client.put('{}/category/{}'.format(
            self.BASE_URL, category_id[0][0]),
             json={
                 'category_name':'Farm Tools',
             },
            headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 202)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['category']['category_name'], "Farm Tools")

    def test_update_category_missing_parameter(self):
        """PUT /product/id - with expected success"""

        self.register_test_admin_account()
        token = self.login_test_admin()

        query = """INSERT INTO category(category_name) VALUES('Tools')"""
        
        database.insert_to_db(query)

        query = """SELECT category_id FROM category WHERE category_name = 'Tools'"""
        category_id = database.select_from_db(query)

        response = self.app_test_client.put('{}/category/{}'.format(
            self.BASE_URL, category_id[0][0]),
            json={},
            headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "Pass update data for category name")

    def test_delete_category(self):
        """DELETE /category/id"""

        self.register_test_admin_account()
        token = self.login_test_admin()

        query = """INSERT INTO category(category_name) VALUES('Tools')""" 
        database.insert_to_db(query)

        query = """SELECT category_id FROM category WHERE category_name = 'Tools'"""
        category_id = database.select_from_db(query)

        response = self.app_test_client.delete('{}/category/{}'.format(
            self.BASE_URL, category_id[0][0]),
            headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "Category deleted successfully")