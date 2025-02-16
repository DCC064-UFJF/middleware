#!/usr/bin/env python
import pika
import sys
from datetime import datetime
import json

# realiza conexão usando ip localhost
connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host='my-rabbit'))
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declara uma filac chamada "task_queue"
channel.queue_declare(queue='task_queue', durable=True)

# emulando um sensor
# circuitos = 
# [
#   {
#     "id": 1,
#     "sensor": [
#       {
#         "id_sensor": 1,
#         "tipo": "Temperatura",
#         "valores": [
#             {"timestamp": 5, "valor": 5},
#              {"timestamp": 5, "valor": 5},
#               {"timestamp": 5, "valor": 5},
#                {"timestamp": 5, "valor": 5}
#         ]
#       },
#       {
#         "id_sensor": 2,
#         "timestamp": 287342323,
#         "tipo": "Atuador",
#         "valor": 0,
#       }
#     ]
#   },
#   {
#     "id": 2,
#     "sensor": [
#       {
#         "id_sensor": 1,
#         "timestamp": 287342323,
#         "tipo": "Temperatura",
#         "valor": 37,
#       }
#     ]
#   }
# ]
 
#  {
#         "id_circuito":''
#         "id_sensor": 1,
#         "tipo": "Temperatura",
#         "valor": 37,
#         "timestamp": 287342323
#       }
 
 

dados_enviados_sensor = {
    "id": 1,
    "device": 
    {
        "id": 19,
        "tipo": "TEMPERATURA",
        "valor": 0,
        "timestamp": datetime.now().isoformat(),
    }
}

message = json.dumps(dados_enviados_sensor).encode()

# publica a mensagem
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    ))

print(f" [x] Sent {message}")
connection.close()