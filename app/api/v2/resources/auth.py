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
                "message": "Kindly enter your credentials"
            }
            ), 400)
        request_email = data["email"].strip()
        request_password = data["password"].strip()
        
        user = users.User_Model.fetch_user(request_email)
        if not user:
            abort(make_response(jsonify(
                message="User not found."), 404))

        user_email = user[0][1]
        user_password = user[0][2]

        if request_email == user_email and check_password_hash(user_password, request_password):
            token = jwt.encode({
                "email": request_email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=3000)
            }, os.getenv('JWT_SECRET_KEY', default='SdaHv342nx!jknr837bjwd?c,lsajjjhw673hdsbgeh'))
            return make_response(jsonify({
                            "message": "Login successful",
                            "token": token.decode("UTF-8")}), 200)

        return make_response(jsonify({
            "message": "Wrong credentials provided"
        }
        ), 403)