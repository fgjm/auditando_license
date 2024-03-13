import sys
import json
from logs import get_error, do_log
from api.models import License
import datetime

def get_response(license_id,licenses):
    status=200
    message ='licenses_obtained'
    if type(licenses)==str:
        status=500
        message ='internal_error'        
    elif not licenses:
        status=400
        message ='user_not_have_licenses' if license_id < 0 else 'license_id_not_found'
    return {
            'message':message, 
            'license_info':licenses,
            'status': status
        }
#


def resolve_get(license_id, user_owner):
    try:        
        licenses = License(license_id).find(user_owner)
        
        return get_response(license_id,licenses)
    except:
        return get_error('resolve_get, controllers',sys.exc_info())

def resolve_post(license_data):
    try:  
        #devolver a <class 'datetime.datetime'>: datetime.datetime.strptime(data, '%Y-%m-%dT%H%M%S.%f')     
        license_data={**license_data, **{
                "createdAt": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f') ,
                "is_active": True, "is_banned": False, "modificated":""
            }
        }
        license=License(0).register(license_data)
        return {
                'message': 'license_created', 
                'license_info':  license,
                'status': 201
            }
    except:
        return get_error('resolve_post, controllers',sys.exc_info())

def resolve_put(license_data):
    try:
        license_data={**license_data, **{
                "modificated": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
            }
        }
        license=License(license_data['license_id']).update(license_data) 
        return {
                'message': 'license_updated', 
                'license_info': license,
                'status': 200
            }
    except:
        return get_error('resolve_put, controllers',sys.exc_info())

def resolve_delete(license_id):
    try:      
        license=License(license_id).delete() 
        return {
                'message': license,                
                'status': 200
            }
    except:
        return get_error('resolve_delete, controllers',sys.exc_info())