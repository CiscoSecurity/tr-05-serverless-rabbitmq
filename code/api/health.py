from lib2to3.pgen2.token import RPAR
from flask import Blueprint
from api.utils import get_jwt, jsonify_data
from api.extensions import http_rpc

health_api = Blueprint('health', __name__)


@health_api.route('/health', methods=['POST'])
def health():
    _ = get_jwt()

    params = {"command": "retrieve_url",
            "url": "http://ifconfig.me", "method": "GET"}
    response = http_rpc.call(params)
    print(response)

    return jsonify_data({'status': 'ok'})
