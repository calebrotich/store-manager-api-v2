"""This module contains objects for products endpoints"""

import os
import jwt
from functools import wraps

from flask import Flask, jsonify, request, abort, make_response
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import common_functions
from ..models import products, sale_orders, users
from ..utils import verify, validator
from .. import database


class Product(Resource):
    """Class contains products endpoints CRUD"""
    
    
    def post(self):
        """POST /products endpoint"""

        # Token verification and admin user determination
        logged_user = verify.verify_tokens()
        common_functions.abort_if_user_is_not_admin(logged_user)
        
        data = request.get_json()
        common_functions.no_json_in_request(data)
        try:
            product_name = data['product_name']
            product_price = data['product_price']
            category = data['category']
        except KeyError:
            # If product is missing required parameter
            common_functions.missing_a_required_parameter()

        verify.verify_post_product_fields(product_price, product_name, category)
        validator.Validator.check_duplication("product_name", "products", product_name)

        added_product = products.Products(product_name=product_name, product_price=product_price,
                                          category=category)
        added_product.save()

        return make_response(jsonify({
            "message": "Product added successfully",
            "product": {
                "product_name": product_name,
                "product_price": product_price,
                "category": category
            }
        }), 201)



    def get(self):
        """GET /products endpoint"""

        verify.verify_tokens()
        
        fetch_products = products.Products()
        fetched_products = fetch_products.fetch_all_products()
        if not fetched_products:
            return make_response(jsonify({
                "message": "There are no products in the store yet",
                }), 404)

        response = jsonify({
            'message': "Successfully fetched all the products",
            'products': fetched_products
            })

        response.status_code = 200
        return response


class SpecificProduct(Resource):
    def get(self, product_id):
        """GET /products/<int:product_id> endpoint"""
        
        verify.verify_tokens()
        query = """SELECT * FROM products WHERE product_id = '{}'""".format(product_id)

        fetched_product = database.select_from_db(query)
        if not fetched_product:
            return make_response(jsonify({
            "message": "Product with id {} is not available".format(product_id),
            }), 400)
        
        return make_response(jsonify({
            "message": "{} retrieved successfully".format(fetched_product[0][1]),
            "product": fetched_product
            }), 200)

    def put(self, product_id):
        """PUT /product/<int:product_id> endpoint"""

        logged_user = verify.verify_tokens()
        common_functions.abort_if_user_is_not_admin(logged_user)

        data = request.get_json()
        try:
            product_name = data['product_name']
            product_price = data['product_price']
            category = data['category']

        except:
            return make_response(jsonify({
                "message":"Pass all the required fields, the ones you wish not"
                           + " to update should still be passed with the same data"
            }), 403)
            
        common_functions.no_json_in_request(data)
        verify.verify_post_product_fields(product_price, product_name, category)

        striped_product_name = data['product_name'].strip()
        striped_category = data['category'].strip()
        validator.Validator.check_duplication("product_name", "products", striped_product_name)

        try:
            product = products.Products(product_id=product_id, product_name=striped_product_name,
                                        product_price=data['product_price'], category=striped_category)
            product.put()
            return make_response(jsonify({
                "message":"Product updated successfully",
                "product": data
            }), 202)
        except:
            return make_response(jsonify({
                "message":"We experienced a problem with the database, login again and re-try"
            }), 500)



