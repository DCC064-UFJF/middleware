#!/usr/bin/env python
import pika
import time
from utils import insert_db
from database.connection import mongo_client
import json

# realiza a conexão usando localhost como ip
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='my-rabbit', port=5672))
channel = connection.channel()

# declara a fila com mesmo nome do publisher
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C') 
sensor_collection = mongo_client['sensor']

# callback que será chamado quando ler uma mensagem
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    msg = body.decode()
    sensor_data = json.loads(msg)
    
    
    new_data = {"timestamp": sensor_data["sensor"]["timestamp"], "valor": sensor_data["sensor"]["valor"]}
    sensor_collection.update_one(
        {"_id": sensor_data["_id"], "sensor.id_sensor": sensor_data["sensor"]["id_sensor"]},  # Encontrar o circuito e sensor de temperatura
        {"$push": {"sensor.$.historico": new_data}}
    )
    
    insert_db(sensor_data) # insere no mongodb 
    
    time.sleep(5) # espera 5 segundos para "fingir" que está processando (RETIRAR DEPOIS)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag) # ack para confirmar consumo da mensagem


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()