from lib2to3.pgen2.token import RPAR
from flask import Blueprint, request
from api.utils import get_jwt, jsonify_data
from api.extensions import http_rpc

route_api = Blueprint('route', __name__)


@route_api.route('/<path:path>', methods=['GET', 'POST', 'HEAD', 'PUT', 'DELETE'])
def catch_all(path):
    payload = get_jwt()
    
    headers = {}
    for (key, value) in request.headers: headers[key] = value

    params = {
            "requested_route": path,
            "headers": headers,
            "jwt": payload,
            "body": request.json,
            "method": request.method
    }

    response = http_rpc.call(params)
    return response
