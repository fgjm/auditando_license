import sys
from api.models.peewee import licenses_neo4j
from logs import get_error

def get_license_user(license_id):
    try:
        response={'response':False}
        license=licenses_neo4j.get_or_none(licenses_neo4j.license_id==license_id)             
        if license:
            if license.users_quantity>0:
                response={'response':True}
    except:
        get_error('get_license_user_quantity',sys.exc_info())
    return response

def update_license_user(license_id):
    try:
        response={'response':False}
        license=licenses_neo4j.get_or_none(licenses_neo4j.license_id==license_id)             
        if not license or license.users_quantity<1:
            return response
        update_user={"users_quantity":license.users_quantity-1}
        license=licenses_neo4j.update(update_user).where(
                licenses_neo4j.license_id==license_id).execute()     
        if license:
            response={'response':True}
    except:
        get_error('update_license_user_quantity',sys.exc_info())
    return response