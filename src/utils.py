import pika

from os import getenv
from dotenv import load_dotenv
load_dotenv()

connection = pika.BlockingConnection(pika.ConnectionParameters(host=getenv('RABBIT_HOST', 'localhost'), port=getenv('RABBIT_PORT', 5672)))
channel = connection.channel()
channel.queue_declare(queue='actuators', durable=True)