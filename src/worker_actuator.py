#!/usr/bin/env python
import pika
import time
import json

from os import getenv
from dotenv import load_dotenv
load_dotenv()

# realiza a conexão
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=getenv('RABBIT_HOST', 'localhost'), port=getenv('RABBIT_PORT', 5672)))
channel = connection.channel()

channel.queue_declare(queue='actuators', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C') 

# callback que será chamado quando ler uma mensagem
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    msg = body.decode()

    sensor_data = json.loads(msg)

    print(sensor_data)
    
    
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag) # ack para confirmar consumo da mensagem


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='actuators', on_message_callback=callback)

channel.start_consuming()