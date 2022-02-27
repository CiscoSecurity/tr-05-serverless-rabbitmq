"""
TODO:

https://github.com/pika/pika/tree/master/examples

- need a better asynchronous consumer/publisher library!!!
- figure out why when a publisher doesn't respond, the original messdage is just sent back (no timeout callback??)
- need better connection handling (timeouts, disconnects, basic ack, etc ...)

"""

import pika
import uuid
import base64
import json
import ssl


class RPCClient(object):
    def __init__(self):
        self.server = None
        self.vhost = None
        self.username = None
        self.password = None

    def disconnect(self):
        self.connection.close()

    def connect(self, token, server, vhost, username, password):
        # setup the connection
        self.server = server
        self.vhost = vhost
        self.username = username
        self.password = password

        self.key = token
        self.context = ssl.create_default_context(
            cafile="cert/cacert.pem")
        self.context.load_cert_chain("cert/cert.pem",
                                     "cert/key.pem")
        self.credentials = pika.PlainCredentials(self.username, self.password)

        self.ssl_options = pika.SSLOptions(self.context, "client")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.server, virtual_host=self.vhost, port=5671, ssl_options=self.ssl_options, credentials=self.credentials))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue=self.key, exclusive=False)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, params):
        self.response = None
        json_bytes = json.dumps(params).encode()
        base64_string = base64.b64encode(json_bytes)
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=base64_string)
        while self.response is None:
            self.connection.process_data_events()

        return base64.b64decode(self.response).decode()
