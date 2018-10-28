"""This module contains objects for saleorders endpoints"""

from flask import Flask, jsonify, request, abort, make_response
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import common_functions
from ..models import products, saleorders
from ..utils import verify
from .. import database

class SaleOrder(Resource):
    """Class contains CRUD definitions

    for saleorders
    """

    def post(self):
        """POST /saleorder endpoint"""

        verify.verify_tokens()

        data = request.get_json()
        common_functions.no_json_in_request(data)
        try:
            product_name = data['product_name']
            product_price = data['product_price']
            quantity = data['quantity']
        except KeyError:
            # If product is missing required parameter
            common_functions.missing_a_required_parameter()

        if not isinstance(product_price, int):
            abort(make_response(jsonify(
                message="Bad request. The product price should be digits"
            ), 400))

        if product_price < 1:
            abort(make_response(jsonify(
                message="Bad request. Price of the product should be a positive integer above 0."
            ), 400))

        if not isinstance(product_name, str):
            abort(make_response(jsonify(
                message="Bad request. Product name should be a string"
            ), 400))


        if not isinstance(quantity, int):
            abort(make_response(jsonify(
                message="Bad request. The quantity should be specified in digits"
            ), 400))
        strip_product_name = product_name.strip()
        sale_order = saleorders.SaleOrder(strip_product_name, product_price, quantity)
        sale_order.save()

        return make_response(jsonify({
            "message": "Checkout complete",
            "saleorder": {
                "product_name": product_name,
                "product_price": product_price,
                "quantity": quantity,
                "amount": (product_price * quantity)
            }
        }), 201)


    def get(self):
        """GET /saleorder endpoint"""

        verify.verify_tokens()
        
        saleorder = saleorders.SaleOrder()
        get_saleorder = saleorder.get()
        if not get_saleorder:
            return make_response(jsonify({
            'message': "No sale orders created yet"
            }), 404)

        response = jsonify({
            'message': "Successfully fetched all the sale orders",
            'sale_orders': get_saleorder
            })
        response.status_code = 200
        return response


class SpecificSaleOrder(Resource):
    """Class contains CRUD definitions

     for saleorders
     """
    def get(self, saleorder_id):
        """GET /saleorder/<int:saleorder_id>"""

        verify.verify_tokens()
        query = """SELECT * FROM saleorders WHERE saleorder_id = '{}'""".format(saleorder_id)
        sale_order = database.select_from_db(query)
        if not sale_order:
            return make_response(jsonify({
                "message": "Sale Order with id {} not found".format(saleorder_id)
            }
            ), 404)

        return make_response(jsonify({
            "message": "Sale order fetched successfully",
            "saleorder": sale_order
        }
        ), 200)