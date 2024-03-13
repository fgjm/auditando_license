"""
Routes
Last modification: 17-06-2023 - Giovanni Junco
"""
from flask import Blueprint, request , make_response
from api.controllers import resolve_get, resolve_post, \
    resolve_put, resolve_delete
from logs import do_log

license_api = Blueprint('license_api', __name__)

@license_api.route("/", methods=["GET"])
def license_get():
    ''' gets the licenses that the user has access to
        Required attributes:
            - user_owner (int): license owner user
            - license_id (int): license identification number
        Returns: 
            - licenses_info (list): all licenses of user
            - message (str): code response to i18n
            - status (int): status codes num'''
    license_id = request.args.get('license_id',-1)
    user_owner = request.args.get('user_owner', -1 )
    data_response= resolve_get(int(license_id), int(user_owner))    
    return make_response(data_response,data_response['status'])

@license_api.route("/", methods=["POST"])
def license_post():
    ''' Create license with user admin
        Required attributes:
            - user_id (int): user owner
        Returns: 
            - licenses_info (list): all licenses of user
            - message (str): code response to i18n
            - status (int): status codes num'''
    data_response= resolve_post(request.json)
    return make_response(data_response,data_response['status'])

@license_api.route("/", methods=["PUT"])
def license_put():
    ''' Update the licenses that the user has access to
        Required attributes:
            - user_id (int): user owner
        Returns: 
            - licenses_info (list): all licenses of user
            - message (str): code response to i18n
            - status (int): status codes num'''
    data_response= resolve_put(request.json)
    return make_response(data_response,data_response['status'])

@license_api.route("/", methods=["DELETE"])
def license_delete():
    ''' Delete the licenses that the user has access to
        Required attributes:
            - user_id (int): user owner
        Returns: 
            - licenses_info (list): all licenses of user
            - message (str): code response to i18n
            - status (int): status codes num'''
    data_response= resolve_delete(request.json['license_id'])
    return make_response(data_response,data_response['status'])
