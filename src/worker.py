#!/usr/bin/env python
import pika
import time
from utils import insert_db
from database.connection import mongo_client
import json

# realiza a conexão usando localhost como ip
connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host='my-rabbit', port=5672))
    pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

db = mongo_client["application"]

def create_sensor_collection():
    validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["id", "tipo", "valor", "timestamp", "circuito_id"],
            "properties": {
                "id": {
                    "bsonType": "int",
                },
                "tipo": {
                    "bsonType": "string",
                },
                "valor": {
                    "bsonType": "double",
                },
                "timestamp": {
                    "bsonType": "string",
                },
                "circuito_id": {
                    "bsonType": "int",
                }
            }
        }
    }

    db.create_collection('sensores', validator=validator)
    db['sensores'].create_index(['id', 'timestamp'], unique=True)

def create_circuito_collection():
    validator = {
    "$jsonSchema": {
            "bsonType": "object",
            "required": ["id"],
            "properties": {
                "id": {
                    "bsonType": "int",
                }
            }
        }
    }

    db.create_collection('circuitos', validator=validator)
    db['circuitos'].create_index(['id'], unique=True)

def create_atuador_collection():
    validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["id", "valor", "timestamp","circuito_id"],
            "properties": {
                "id": {
                    "bsonType": "int",
                },
                "valor": {
                    "bsonType": "int",
                },
                "timestamp": {
                    "bsonType": "string",
                },
                "circuito_id": {
                    "bsonType": "int",
                }
            }
        }
    }

    db.create_collection('atuadores', validator=validator)
    db['atuadores'].create_index(['id', 'timestamp'], unique=True)

# declara a fila com mesmo nome do publisher
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C') 

# callback que será chamado quando ler uma mensagem
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    msg = body.decode()

    sensor_data = json.loads(msg)
    
    if not db['circuitos'].find_one({'id': sensor_data['id']}):
        db["circuitos"].insert_one({
            "id": sensor_data["id"]
        })

    if sensor_data["device"]["tipo"] == "atuador":
        db["atuadores"].insert_one({
            'id': sensor_data["device"]["id"],
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