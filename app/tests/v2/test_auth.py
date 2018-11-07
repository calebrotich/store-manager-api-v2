"""Module contains tests to endpoints that 

are used for user registration and authentication
"""

import json

from . import base_test
from . import common_functions
from app.api.v2 import database

class TestAuth(base_test.TestBaseClass):
    """ Class contains tests for auth endpoints """

    def test_missing_token(self):
        """Test GET /products - when token is missing"""

        self.register_test_admin_account()
        token = ""

        response = self.app_test_client.get(
            '{}/products'.format(self.BASE_URL),
            headers=dict(Authorization=token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(common_functions.convert_response_to_json(
            response)["Message"], "You need to login")

    def test_missing_token_user(self):
        """Test GET /products - when user who generated token is missing"""

        self.register_test_admin_account()
        token = self.login_test_admin()

        query = """DELETE FROM users"""
        database.insert_to_db(query)

        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json=self.PRODUCT, headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 406)
        self.assertEqual(common_functions.convert_response_to_json(
            response)["message"], "The token is invalid since it is not associated to any account")

    def test_invalid_token(self):
        """Test GET /products - when token is missing"""

        self.register_test_admin_account()
        token = "sample_invalid-token-afskdghkfhwkedaf-ksfakjfwey"

        response = self.app_test_client.get(
            '{}/products'.format(self.BASE_URL),
            headers=dict(Authorization=token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(common_functions.convert_response_to_json(
            response)["Message"], "The token is either expired or wrong")

    def test_add_new_user(self):
        token = self.login_test_admin()

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "test_add_new_user@gmail.com",
        "role": "Admin",
        "password": "Password12#"
        }, 
        headers=dict(Authorization=token),
        content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['user']['email'], "test_add_new_user@gmail.com")
        self.assertEqual(res.status_code, 202)

    def test_add_new_user_no_data(self):
        token = self.login_test_admin()

        res = self.app_test_client.post("api/v2/auth/signup",
        json={

        }, 
        headers=dict(Authorization=token),
        content_type='application/json')

        data = json.loads(res.data.decode())
        self.assertEqual(data['message'], "Missing required credentials")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_missing_data(self):
        token = self.login_test_admin()
        res = self.app_test_client.post("api/v2/auth/signup",
        json={
            "email": "",
            "role": "Admin",
            "password": "Password12#"
             }, 
        headers=dict(Authorization=token),
        content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['message'], "Please supply a valid email")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_missing_key(self):
        token = self.login_test_admin()

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
            "role": "Admin",
            "password": "Password12#"
             }, 
        headers=dict(Authorization=token),
        content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['message'], "Please supply an email to be able to register an attendant")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_invalid_email(self):
        token = self.login_test_admin()

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "test_add_new_user",
        "role": "Admin",
        "password": "Password12#"
        }, 
        headers=dict(Authorization=token),
        content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['message'], "Please supply a valid email")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_no_digit_password(self):
        token = self.login_test_admin()

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "test_add_new_user_invalid_email@gmail.com",
        "role": "Admin",
        "password": "No#digit"
        }, 
        headers=dict(Authorization=token),
        content_type='application/json')

        data = json.loads(res.data.decode())
        self.assertEqual(data['message'], "Password must have a digit")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_short_password(self):
        token = self.login_test_admin()

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "test_add_new_user_invalid_email@gmail.com",
        "role": "Admin",
        "password": "Shor#"
        }, 
        headers=dict(Authorization=token),
        content_type='application/json')

        data = json.loads(res.data.decode())
        self.assertEqual(data['message'], "Password must be long than 6 characters or less than 12")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_no_special_ch_password(self):
        token = self.login_test_admin()

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "test_add_new_user_invalid_email@gmail.com",
        "role": "Admin",
        "password": "NoSplCh12"
        }, 
        headers=dict(Authorization=token),
        content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['message'], "Password must have a special charater")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_no_upper_case_password(self):
        token = self.login_test_admin()

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "test_add_new_user_invalid_email@gmail.com",
        "role": "Admin",
        "password": "noupper12#"
        }, 
        headers=dict(Authorization=token),
        content_type='application/json')

        data = json.loads(res.data.decode())
        self.assertEqual(data['message'], "Password must have an upper case character")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_no_lower_case_password(self):
        token = self.login_test_admin()

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "test_add_new_user_invalid_email@gmail.com",
        "role": "Admin",
        "password": "NOLOWER12#"
        }, 
         headers=dict(Authorization=token),
        content_type='application/json')

        data = json.loads(res.data.decode())
        self.assertEqual(data['message'], "Password must have a lower case character")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_existing(self):
        """Test POST /auth/signup"""
        self.register_test_admin_account()
        response = self.register_test_admin_account()
        data = json.loads(response.data.decode())

        self.assertEqual(data['message'], "Record already exists in the database")
        self.assertEqual(response.status_code, 400)
 
    def test_login_existing_user(self):
        self.register_test_admin_account()
        resp = self.app_test_client.post("api/v2/auth/login",
        json={
            "email": "user@gmail.com",
            "password": "Password12#"
        },
        headers={
        "Content-Type": "application/json"
        })

        self.assertTrue(common_functions.convert_response_to_json(
        resp)['token'])
        self.assertTrue(common_functions.convert_response_to_json(
        resp)['message'], "You are successfully logged in!")
        self.assertEqual(resp.status_code, 200)

    def test_login_no_credentials(self):
        self.register_test_admin_account()
        resp = self.app_test_client.post("api/v2/auth/login",
        json={

        },
        headers={
        "Content-Type": "application/json"
        })

        self.assertTrue(common_functions.convert_response_to_json(
        resp)['message'], "Kindly enter your credentials")
        self.assertEqual(resp.status_code, 400)

    def test_login_wrong_password(self):
        self.register_test_admin_account()
        resp = self.app_test_client.post("api/v2/auth/login",
        json={
            "email": "user@gmail.com",
            "password": "neverexpecteduser"
        },
        headers={
        "Content-Type": "application/json"
        })

        self.assertTrue(common_functions.convert_response_to_json(
        resp)['message'], "Wrong credentials provided")
        self.assertEqual(resp.status_code, 403)

    def test_login_non_existant_user(self):
        self.register_test_admin_account()
        resp = self.app_test_client.post("api/v2/auth/login",
        json={
            "email": "non_matching_credentials_user_1018@gmail.com",
            "password": "neverexpecteduser"
        },
        headers={
        "Content-Type": "application/json"
        })

        self.assertEqual(common_functions.convert_response_to_json(
        resp)['message'], "Try again. E-mail or password is incorrect!")

    def test_abort_if_user_is_not_admin(self):
        self.register_test_admin_account()
        self.register_test_attendant_account()
        token = self.login_test_attendant()

        response = self.app_test_client.post('{}/products'.format(
            self.BASE_URL), json={
                'product_id': 1, 'product_name': "Hammer", 'product_price': 200, 'category': 200
                }, headers=dict(Authorization=token),
                content_type='application/json')

        self.assertTrue(common_functions.convert_response_to_json(
        response)['message'], "Unauthorized. This action is not for you")
        self.assertEqual(response.status_code, 401)


    def test_logout(self):
        token = self.login_test_admin()

        response = self.app_test_client.post('{}/auth/logout'.format(
            self.BASE_URL), headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(common_functions.convert_response_to_json(
            response)['message'], "user@gmail.com Logged out successfully"
        )
    