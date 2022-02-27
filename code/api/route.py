from lib2to3.pgen2.token import RPAR
from flask import Blueprint, request, current_app
from api.utils import get_jwt, jsonify_data
from api.extensions import http_rpc
from api.errors import AuthorizationError

route_api = Blueprint('route', __name__)

# catchall
@route_api.route('/<path:path>', methods=['GET', 'POST', 'HEAD', 'PUT', 'DELETE'])
def catch_all(path):
    payload = get_jwt()

    headers = {}
    for (key, value) in request.headers:
        headers[key] = value
        
    # ensure the client token & password was sent
    if 'client_token' in payload and 'client_password' in payload:
        token = payload['client_token']
    else:
        raise AuthorizationError('Client Token/Password missing.')

    # connect to the AMQP server
    http_rpc.connect(token, current_app.config['AMQP_SERVER'],
        current_app.config['AMQP_VHOST'], 
        current_app.config['AMQP_USERNAME'],
        current_app.config['AMQP_PASSWORD'])

    params = {
        "requested_route": path,
        "headers": headers,
        "jwt": payload,
        "body": request.json,
        "method": request.method
    }
    
    response = http_rpc.call(params)    # blocking - do the request
    http_rpc.disconnect()   # close the connection
    return response
