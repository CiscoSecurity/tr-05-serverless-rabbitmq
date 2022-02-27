import json


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings["VERSION"]
    AMQP_SERVER = 'rabbitmq.lan.cyberthre.at'
    AMQP_VHOST = '/'
    AMQP_USERNAME = 'relay'
    AMQP_PASSWORD = 'relay'