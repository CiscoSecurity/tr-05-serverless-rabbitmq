"""Initialize any app extensions."""
from lib.amqp import RPCClient
from flask import current_app

http_rpc = RPCClient()
