import sys
from api.models import License
from logs import get_error

def get_license_user(license_id):
    try:
        response={'response':False}
        licenses = License(license_id).find()
        print('get_license_user: ',licenses)
        if licenses:
            if licenses[0]['users_quantity']>0:
                response={'response':True}
    except:
        get_error('get_license_user_quantity, socket.py',sys.exc_info())
    return response

def update_license_user(license_id):
    try:
        response={'response':False}
        licenses = License(license_id).find()             
        if not licenses or licenses[0]['users_quantity']<1:
            return response
        licenses[0]['users_quantity']-=1
        print('Update socket:',licenses[0], license_id)
        license=License(license_id).update(licenses[0])   
        if license:
            response={'response':True}
    except:
        get_error('update_license_user_quantity, socket.py',sys.exc_info())
    return response