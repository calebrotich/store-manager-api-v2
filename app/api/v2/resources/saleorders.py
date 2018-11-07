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
        user_id = verify.verify_tokens()[1]

        data = request.get_json()
        common_functions.no_json_in_request(data)
        try:
            items = data['items']
        except KeyError:
            return make_response(jsonify({
                "message":"list of items missing"
            }), 403)
        if not isinstance(items, (list, )):
            abort(make_response(jsonify(
                message="The value should be a list of dictionaries"
                ), 400))

        totalAmount = 0
        saleorder = saleorders.SaleOrder(amount=totalAmount, made_by=user_id)
        saleorder.save()

        query = """SELECT saleorder_id from saleorders WHERE amount = 0
        """
        saleorder_id = database.select_from_db(query)[0]['saleorder_id']
        for item in items:
            try:
                product = item['product']
            except:
                return make_response(jsonify({
                    "message":"Kindly specify the product you want to buy"
                }), 403)            
            try:
                quantity = item['quantity']
            except:
                return make_response(jsonify({
                    "message":"Kindly specify the quantity of the product you want"
                }), 403) 

            if not isinstance(product, int):
                rollback_saleorder = saleorders.SaleOrder(saleorder_id=saleorder_id)
                rollback_saleorder.rollback_saleorder()
                abort(make_response(jsonify(
                    message="Please select the a product you want to purchase"
                ), 400))

            if not isinstance(quantity, int):
                rollback_saleorder = saleorders.SaleOrder(saleorder_id=saleorder_id)
                rollback_saleorder.rollback_saleorder()
                abort(make_response(jsonify(
                    message="Please have a number for the quantity value"
                ), 400))

            if quantity < 1:
                rollback_saleorder = saleorders.SaleOrder(saleorder_id=saleorder_id)
                rollback_saleorder.rollback_saleorder()
                abort(make_response(jsonify(
                    message="Please have a quantity value over 0"
                ), 400))

            query = """SELECT * FROM products WHERE product_id = '{}'""".format(product)
            product_exists = database.select_from_db(query)
            if product_exists:
                product_name = product_exists[0]['product_name']
                product_price = product_exists[0]['product_price']
                inventory = product_exists[0]['inventory']
                if inventory == 0:
                    rollback_saleorder = saleorders.SaleOrder(saleorder_id=saleorder_id)
                    rollback_saleorder.rollback_saleorder()
                    return abort(make_response(jsonify(
                    message="Please eliminate {} from your sale. It is currently out of stock".format(product_name)
                    ), 400))

                if quantity > inventory:
                     rollback_saleorder = saleorders.SaleOrder(saleorder_id=saleorder_id)
                     rollback_saleorder.rollback_saleorder()

                     return abort(make_response(jsonify(
                     message="Our current stock cannot serve an order of {}. You can currently order a maximum of {} for the product '{}'".format(quantity, inventory, product_name)
                     ), 400))                   

                totalAmount += (product_price * quantity)
                sale_item = saleorders.SaleItems(saleorder_id=saleorder_id, product=product, quantity=quantity)
                sale_item.save()
                updated_inventory = inventory - quantity
                product_to_update = products.Products(product_id=product ,inventory=updated_inventory)
                product_to_update.deduct_inventory()

            if not product_exists:
                rollback_saleorder = saleorders.SaleOrder(saleorder_id=saleorder_id)
                rollback_saleorder.rollback_saleorder()
                return abort(make_response(jsonify({
                    "message": "Product with id {} is not available in the store".format(product)
                }), 404))

        update_amount_query = """UPDATE saleorders SET amount = {} WHERE saleorder_id = {}""".format(totalAmount, saleorder_id)
        database.insert_to_db(update_amount_query)

        return make_response(jsonify({
            "message": "Checkout complete",
            "items_sold": items,
            "total_amount": totalAmount
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