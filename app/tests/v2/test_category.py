"""Module defines test cases for product category"""

from . import base_test
from app.api.v2 import database
from . import common_functions


class TestCategory(base_test.TestBaseClass):
    """Class defines CRUD methods for product category"""


    def test_post_category(self):
        """POST /category"""
        response = self.app_test_client.post('{}/category'.format(
            self.BASE_URL), json={
                'category_name': 'Accessories'
            }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(common_functions.convert_response_to_json(
            response)["message"], "Category created successfully")

    def test_post_category_missing_parameter(self):
        """POST /category"""
        response = self.app_test_client.post('{}/category'.format(
            self.BASE_URL), json={}, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(common_functions.convert_response_to_json(
            response)["message"], "Please provide a name for the category")


    def test_get_all_categories(self):
        query = """INSERT INTO category(category_name) VALUES('Accessories')"""
        
        database.insert_to_db(query)
        response = self.app_test_client.get("{}/category".format(
            self.BASE_URL), headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
            response)["message"], "Categories fetched successfully")

    def test_get_all_categories_no_data(self):
        query = """DELETE FROM category"""
        database.insert_to_db(query)
        response = self.app_test_client.get("{}/category".format(
            self.BASE_URL), headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(common_functions.convert_response_to_json(
            response)["message"], "No categories created yet")

    def test_update_category(self):
        """PUT /product/id - with expected success"""
        query = """INSERT INTO category(category_name) VALUES('Accessories')"""     
        database.insert_to_db(query)
        query = """SELECT category_id FROM category WHERE category_name = 'Accessories'"""
        category_id = database.select_from_db(query)

        response = self.app_test_client.put('{}/category/{}'.format(
            self.BASE_URL, category_id[0]['category_id']),
             json={
                 'category_name':'Electronics',
             },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 202)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['category']['category_name'], "Electronics")

    def test_update_category_missing_parameter(self):
        """PUT /product/id - with expected success"""
        query = """INSERT INTO category(category_name) VALUES('Electronics')"""     
        database.insert_to_db(query)

        query = """SELECT category_id FROM category WHERE category_name = 'Electronics'"""
        category_id = database.select_from_db(query)

        response = self.app_test_client.put('{}/category/{}'.format(
            self.BASE_URL, category_id[0]['category_id']),
            json={},
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "Pass update data for category name")

    def test_update_category_name_integer(self):
        """PUT /product/id - with expected success"""
        query = """INSERT INTO category(category_name) VALUES('Electronics')"""    
        database.insert_to_db(query)

        query = """SELECT category_id FROM category WHERE category_name = 'Electronics'"""
        category_id = database.select_from_db(query)

        response = self.app_test_client.put('{}/category/{}'.format(
            self.BASE_URL, category_id[0]['category_id']),
            json={
                "category_name": 4
            },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "Category name should be a string")

    def test_delete_category(self):
        """DELETE /category/id"""

        query = """INSERT INTO category(category_name) VALUES('Electronics')""" 
        database.insert_to_db(query)

        query = """SELECT category_id FROM category WHERE category_name = 'Electronics'"""
        category_id = database.select_from_db(query)

        response = self.app_test_client.delete('{}/category/{}'.format(
            self.BASE_URL, category_id[0]['category_id']),
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "Category deleted successfully")