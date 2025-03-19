#!/usr/bin/env python
import pika
import time
from database.connection import mongo_client
import json

from os import getenv
from dotenv import load_dotenv
load_dotenv()

# realiza a conexão
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=getenv('RABBIT_HOST', 'localhost'), port=getenv('RABBIT_PORT', 5672))
)
channel = connection.channel()

# CRIA BANCO DE DADOS CHAMADO "application", e cria coleções "circuitos", "sensores", "atuadores"
db = mongo_client["application"]

# declara a fila com mesmo nome do publisher
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C') 

# callback que será chamado quando ler uma mensagem
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    msg = body.decode()

    sensor_data = json.loads(msg)
    
    # Se o valor de id do circuito ainda não foi inserido, ele será inserido com insert_one
    if not db['circuitos'].find_one({'id': sensor_data['id']}):
        db["circuitos"].insert_one({
            "id": sensor_data["id"]
        })

    # Verifica se tipo é atuador, para inserir um atuador. Caso contrário, insere um sensor.
    if sensor_data["device"]["tipo"] == "atuador":
        db["atuadores"].insert_one({
            'id': sensor_data["device"]["id"],
            'tipo': sensor_data["device"]["tipo"],
            'valor': sensor_data["device"]["valor"],
            'timestamp': sensor_data["device"]["timestamp"],
            'circuito_id': sensor_data["id"]
        })
    else: 
        db["sensores"].insert_one({
            'id': sensor_data["device"]["id"],
            'tipo': sensor_data["device"]["tipo"],
            'valor': sensor_data["device"]["valor"],
            'timestamp': sensor_data["device"]["timestamp"],
            'circuito_id': sensor_data["id"]
        })
    
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag) # ack para confirmar consumo da mensagem


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()