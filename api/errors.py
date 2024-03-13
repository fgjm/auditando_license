"""
Error Handler
Last modification: 19-03-2023 - Giovanni Junco
"""
import sys
from flask import json, make_response, jsonify
from werkzeug.exceptions import HTTPException
from logs import do_log

# define an error handling function
def init_handler(app):
    """ catch every type of exception """
    @app.errorhandler(Exception)
    def handle_exception(event):
        """Log error!   """
        error = sys.exc_info()
        error=str(error[0])+' '+str(error[1])
        # return json response of error
        if isinstance(event, HTTPException):
            response = event.get_response()
            # replace the body with JSON
            response.data = json.dumps({
                "code": event.code,
                "name": event.name,
                "message": event.description,
            })
        else:
            response = make_response(jsonify({
                "message": 'Something went wrong',
                "errors":  error,
                "error":  error
                }), 500)
        # add the CORS header
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.content_type = "application/json"
        do_log(' Media:',error,'Error Handler','warning')
        return response
