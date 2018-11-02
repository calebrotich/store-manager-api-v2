import os
import jwt
from functools import wraps

from flask import Flask, jsonify, request, abort, make_response
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import common_functions
from ..models import products, saleorders, users, category
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
            return make_response(jsonify({
                        "message": "Please provide a name for the category"
                        }), 400)

        if not isinstance(category_name, str):
            return make_response(jsonify({
                        "message": "Category name should be a string"
                        }), 406)            

        validator.Validator.check_duplication("category_name", "category", category_name)

        added_category = category.Category(category_name=category_name)
        added_category.save()

        return make_response(jsonify({
            "message": "Category created successfully",
            "category": {
                "category_name": category_name
            }
        }), 201)


    def get(self):
        """GET /category"""
        logged_user = verify.verify_tokens()
        common_functions.abort_if_user_is_not_admin(logged_user)
        fetch_category = category.Category()
        fetched_categories = fetch_category.get()

        if not fetched_categories:
            return make_response(jsonify({
                "message": "No categories created yet"
            }), 404)

        response = make_response(jsonify({
            "message": "Categories fetched successfully",
            "categories": fetched_categories
        }), 200)

        return response

class SpecificCategory(Resource):
    """Handles CRUD on a specific category"""


    def put(self, category_id):
        """PUT /product/<int:product_id> endpoint"""

        logged_user = verify.verify_tokens()
        common_functions.abort_if_user_is_not_admin(logged_user)

        data = request.get_json()
        try:
            category_name = data['category_name']

        except:
            return make_response(jsonify({
                "message": "Pass update data for category name"
            }), 403)
            
        common_functions.no_json_in_request(data)
        # verify.verify_post_product_fields(product_price, product_name, category)
        try:
            striped_category_name = category_name.strip()
        except:
            return make_response(jsonify({
                "message": "Category name should be a string"
            }), 403)

        validator.Validator.check_duplication("category_name", "category", striped_category_name)

        update_category = category.Category(category_id=category_id, category_name=striped_category_name)
        update_category.put()
        return make_response(jsonify({
            "message":"Product updated successfully",
            "category": data
        }), 202)


    def delete(self, category_id):
        logged_user = verify.verify_tokens()
        common_functions.abort_if_user_is_not_admin(logged_user)
        query="""SELECT * FROM category WHERE category_id = {}""".format(category_id)
        cat_exists = database.select_from_db(query)
        if not cat_exists:
            return make_response(jsonify({
                "message":"No need for that. Category with id {} does not exist".format(category_id),
            }), 404)
        fetch_category = category.Category(category_id=category_id)
        fetch_category.delete()

        return make_response(jsonify({
            "message": "Category deleted successfully"
        }), 200)