import os
import jwt
from functools import wraps

from flask import request, make_response, jsonify, abort
from ..models import users
from .. import database


def verify_tokens():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
    if not token:
        abort(make_response(jsonify({
                                "Message": "You need to login"}), 401))

    query = """SELECT token FROM blacklist WHERE  token = '{}'""".format(token)
    blacklisted = database.select_from_db(query)
    if blacklisted:
        abort(make_response(jsonify({
                        "Message": "Kindly login again"}), 401))
    try:
        data = jwt.decode(token, os.getenv('JWT_SECRET_KEY', default='SdaHv342nx!jknr837bjwd?c,lsajjjhw673hdsbgeh'))
        return data["email"]

    except:
        abort(make_response(jsonify({
            "Message": "The token is either expired or wrong"
        }), 403))    



def verify_post_product_fields(product_price=None, category=None, inventory=None, min_quantity=None, product_name=None):
    if not isinstance(product_price, int) and product_price:
        abort(make_response(jsonify(
            message="Product price should be an integer"
        ), 400))

    if product_price < 1:
        abort(make_response(jsonify(
            message="Price of the product should be a positive integer above 0."
        ), 400))

    if not isinstance(inventory, int) and inventory:
        abort(make_response(jsonify(
            message="Inventory should be an integer"
        ), 400))

    if not isinstance(min_quantity, int) and min_quantity:
        abort(make_response(jsonify(
            message="Minimum quantity should be an integer"
        ), 400))

    if not isinstance(category, str) and category:
        abort(make_response(jsonify(
            message="Category should be an string referencing the category table"
        ), 400))

    if not isinstance(product_name, str) and product_name:
        abort(make_response(jsonify(
            message="Product name should be a string"
        ), 400))

    if product_name == "":
        abort(make_response(jsonify(
            message="Product name can not be blank"
        ), 400))