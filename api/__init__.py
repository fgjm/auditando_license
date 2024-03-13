"""
load ap License
Last modification: 05-03-2023 - Giovanni Junco
"""
import sys
from flask import Flask, send_from_directory
import os
from flask_cors import CORS
from flask_socketio import SocketIO
import api.errors as error
from .routes import license_api
from .docs import swaggerui_blueprint
from flask_socketio import send
from api.controllers.socket import get_license_user, update_license_user

app = Flask(__name__)

socketio = SocketIO(app)
app.register_blueprint(license_api, url_prefix='/license')

app.register_blueprint(swaggerui_blueprint, url_prefix="/api/docs/")

@app.route("/docs/swagger.json")
def specs():
    return send_from_directory(os.getcwd()+'/api/docs/', "swagger.json")

@socketio.on('license_capacity')
def handle_license_capacity(data):
    print('received license_capacity: ', data)    
    send(get_license_user(data['license_id']))

@socketio.on('update_license_users')
def handle_update_license(data):
    print('received update_license_users: ', data)    
    send(update_license_user(data['license_id']))  
    
@app.route('/')
def ref():
    ''' Info micro_service'''
    return {
        "Author": "Giovanni Junco",
        "project": "Multimedia Backend",
        "version": "0.1",
        "contributor": ["Giovanni Junco"]
    }

from api.utilities import begin_job


begin_job()

@app.after_request
def after_request(response):
    ''' analisa si la conexion a neo4j no esta cerrado, cuenta 30 segundos de inactividad para cerrarla'''
    try:   
        from api.models import driver
        if not driver._closed:       
            begin_job()
        return response
    except:
        print('prompt, utilies',sys.exc_info())
    

@app.before_request
def before_request():
    ''' start daemon'''
    print('Before')

#Cross-Origin Resource Sharing: integrated access with the front-end
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#handling unexpected errors like unknown urls - errors.py
error.init_handler(app)
