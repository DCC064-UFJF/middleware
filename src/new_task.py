#!/usr/bin/env python
import pika
import sys
from datetime import datetime

# realiza conexão usando ip localhost
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declara uma filac chamada "task_queue"
channel.queue_declare(queue='task_queue', durable=True)

# emulando um sensor
message = f"{datetime.now()},temperature,21"
    
# publica a mensagem
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message.encode(),
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    ))

print(f" [x] Sent {message}")
connection.close()