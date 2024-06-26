import pika
from bson import ObjectId
from mongoengine import connect

from app.model import Contact
from configparser import ConfigParser

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

config = ConfigParser()
config.read('config.ini')

mongo_uri = config['Database']['uri']
connect(host=mongo_uri)

def send_email_stub(contact):
    print(f"Sending email to {contact.email}")

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=ObjectId(contact_id)).first()
    if contact:
        send_email_stub(contact)
        contact.is_sent = True
        contact.save()
        print(f" [x] Updated status for contact: {contact.fullname}")

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
