import pika
from faker import Faker
from app.model import Contact
from configparser import ConfigParser
from mongoengine import connect

config = ConfigParser()
config.read('config.ini')
mongo_uri = config['Database']['uri']
connect(host=mongo_uri)

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

fake = Faker()

def insert_data():
    contact = Contact(fullname=fake.name(), email=fake.email())
    contact.save()
    print("Save successfully")
    return str(contact.id)

contact_id = insert_data()

if channel.basic_publish(exchange='', routing_key='email_queue', body=contact_id):
    print(f" [x] Sent message with contact_id: {contact_id}")

connection.close()
