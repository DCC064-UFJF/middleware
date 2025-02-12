#!/usr/bin/env python
import pika
import time
from utils import insert_db

# realiza a conexão usando localhost como ip
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='my-rabbit', port=5672))
channel = connection.channel()

# declara a fila com mesmo nome do publisher
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C') 

# callback que será chamado quando ler uma mensagem
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    msg = body.decode()
    segs = msg.split(",")
    sensor_data = {
        "timestamp": segs[0],
        "type": segs[1],
        "value": segs[2],
    }
    insert_db(sensor_data) # insere no mongodb 
    
    time.sleep(5) # espera 5 segundos para "fingir" que está processando (RETIRAR DEPOIS)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag) # ack para confirmar consumo da mensagem


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()