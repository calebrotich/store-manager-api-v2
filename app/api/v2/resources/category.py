import os
import jwt
from functools import wraps

from flask import Flask, jsonify, request, abort, make_response
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import common_functions
from ..models import products, sale_orders, users, category
from ..utils import verify, validator
from .. import database

class ProductCategory(Resource):
    
    def post(self):
        """POST /category endpoint"""

        # Token verification and admin user determination
        logged_user = verify.verify_tokens()
        common_functions.abort_if_user_is_not_admin(logged_user)
        
        data = request.get_json()
        common_functions.no_json_in_request(data)
        try:
            category_name = data['category_name']
        except KeyError:
            # If product is missing required parameter
            common_functions.missing_a_required_parameter()

        validator.Validator.check_duplication("category_name", "category", category_name)

        added_category = category.Category(category_name=category_name)
        added_category.save()

        return make_response(jsonify({
            "message": "Category created successfully",
            "category": {
                "category_name": category_name
            }
        }), 201)