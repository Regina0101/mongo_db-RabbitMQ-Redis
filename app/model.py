from mongoengine import Document, StringField, BooleanField, EmailField, connect
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
mongo_uri = config['Database']['uri']
connect(host=mongo_uri)

class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True)
    is_sent = BooleanField(default=False)
