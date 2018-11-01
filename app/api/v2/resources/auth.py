"""This module contains objects for auth endpoints"""

import os
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from flask import Flask, jsonify, request, make_response, abort
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)

from instance import config
from ..utils.validator import Validator
from ..models import users
from ..utils import verify

class SignUp(Resource):
    """Signup class"""

    def post(self):
        """POST /auth/login"""

        data = request.get_json()
        if not data:
            return make_response(jsonify({
                                    "message": "Missing required credentials"
                                    }), 400)
        try:
            email = data["email"].strip()
            request_password = data["password"].strip()
            request_role = data["role"].strip()
        except KeyError:
            return make_response(jsonify({
                        "message": "Missing required credentials"
                        }), 400)

        Validator.validate_credentials(self, data)
        Validator.check_duplication("email", "users", email)
        hashed_password = generate_password_hash(request_password, method='sha256')
        user = users.User_Model(email, hashed_password, request_role)
        user.save()
        return make_response(jsonify({
            "message": "Account created successfully",
            "user": {
                "email": email,
                "role": request_role
            }
        }), 202)


class Login(Resource):
    """Login class"""

    def post(self):
        """POST /auth/signup"""

        data = request.get_json()          
        if not data:
            return make_response(jsonify({
                "message": "Kindly provide an email and a password to login"
            }
            ), 400)

        try:
            request_mail = data["email"]
        except:
            return make_response(jsonify({
                "message": "Kindly provide an email address to log in"
             }), 400)

        if not isinstance(data['email'], str):
             return make_response(jsonify({
                "message": "E-mail should be a string"
            }
            ), 406)

        if not isinstance(data['password'], str):
             return make_response(jsonify({
                "message": "Password should be a string"
            }
            ), 406)

        request_email = request_mail.strip()
        try:
            request_password = data["password"]
        except:
            return make_response(jsonify({
                "message": "Kindly provide a password to log in"
             }), 400)
                    
        user = users.User_Model.fetch_user(request_email)

        if user and request_email == user[0]['email'] and check_password_hash(user[0]['password'], request_password):
            token = jwt.encode({
                "email": request_email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=3000)
            }, os.getenv('JWT_SECRET_KEY', default='SdaHv342nx!jknr837bjwd?c,lsajjjhw673hdsbgeh'))
            return make_response(jsonify({
                            "message": "Login successful",
                            "token": token.decode("UTF-8")}), 200)

        return make_response(jsonify({
            "message": "Try again. E-mail or password is incorrect!"
        }
        ), 403)


class Logout(Resource):
    """Logout class"""

    def post(self):
        """POST /auth/logout"""
        
        logged_user = verify.verify_tokens()
        token = request.headers['Authorization']
        user = users.User_Model(token=token)
        user.logout()

        return make_response(jsonify({
            'message': '{} Logged out successfully'.format(logged_user)
        }))
