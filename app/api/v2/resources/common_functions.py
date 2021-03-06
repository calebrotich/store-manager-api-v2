"""This module contains re-usable functions"""

from datetime import datetime

from flask import abort, jsonify, make_response

from ..models import products, saleorders, users
from .. import database

def no_json_in_request(data):
    """Aborts if the data does

    not contain a valid json object      
    """
        
    if data is None:
        # If a json was not obtained from the request
        abort(make_response(jsonify(
            message="Request data must be in json format"), 400))


def missing_a_required_parameter():
    """Aborts if request data is missing a

    required argument
    """
    abort(make_response(jsonify(
        message="Request missing a required argument"), 400))


def abort_if_user_is_not_admin(user):
    query = """SELECT role FROM users WHERE email = '{}'""".format(user)
    user_role = database.select_from_db(query)
    print(user_role)
    if user_role and user_role[0]['role'] != "admin":
        return abort(make_response(jsonify(
            message="Unauthorized. This action is not for you"
        ), 401))
    elif not user_role:
        return abort(make_response(jsonify(
            message="The token is invalid since it is not associated to any account"
         ), 406))
