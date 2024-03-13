import sys
from logs import get_error, do_log
from api.models.peewee import licenses_neo4j
import datetime
from playhouse.shortcuts import model_to_dict

def resolve_get(user_id):
    try:
        licenses = licenses_neo4j.select().where( 
                                    licenses_neo4j.user_owner == user_id
                                ).dicts()
        return {
                'message': 'licenses_obtained', 
                'license_info':[row for row in licenses],
                'status': 200
            }
    except:
        return get_error('resolve_get, controllers',sys.exc_info())

def resolve_post(user_info):
    try:
        license=licenses_neo4j.create(
            orders_quantity = user_info['orders_quantity'],
            users_quantity = user_info['users_quantity'],
            license_name  = user_info['license_name'],
            pesos_col = user_info['pesos_col'],
            user_owner = user_info['user_owner'],            
            created=datetime.datetime.now(datetime.timezone.utc)            
        )
        return {
                'message': 'license_created', 
                'license_info':model_to_dict(license),
                'status': 201
            }
    except:
        return get_error('resolve_post, controllers',sys.exc_info())

def resolve_put(data):
    try:
        valid_field = ["orders_quantity", "users_quantity", "license_name", 
                        "pesos_col", "user_owner"]
        # Get only allowed information, not permit change in 
        user_info = {k: v for k, v in data.items() if k in valid_field}       
        license=licenses_neo4j.update(user_info).where(
                licenses_neo4j.license_id==data['license_id']).execute()       
        license=licenses_neo4j.get_or_none(licenses_neo4j.license_id==license)
        license = model_to_dict(license) if license else ''        
        return {
                'message': 'license_updated', 
                'license_info': license,
                'status': 200
            }
    except:
        return get_error('resolve_put, controllers',sys.exc_info())

def resolve_delete(license_id):
    try:
        licenses_neo4j.delete().where(
            licenses_neo4j.license_id == license_id
        ).execute()
        return {
                'message': 'license_deleted',                
                'status': 500
            }
    except:
        return get_error('resolve_delete, controllers',sys.exc_info())