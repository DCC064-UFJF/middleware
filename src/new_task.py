#!/usr/bin/env python
import pika
from datetime import datetime
import json
import random

from os import getenv
from dotenv import load_dotenv
load_dotenv()

# realiza conexão
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=getenv('RABBIT_HOST', 'localhost'), port=getenv('RABBIT_PORT', 5672)))
channel = connection.channel()

# declara uma filac chamada "task_queue"
channel.queue_declare(queue='task_queue', durable=True)

types = ["Temperatura", "Umidade", "Pressao", "atuador"]
id_circuit = random.randint(1, 4)
tipo = random.choice(types)

if tipo == "atuador":
    id_device = random.randint(7, 12)
    valor = random.randint(0, 1)
else:
    id_device = random.randint(1, 6)
    valor = random.uniform(30, 40)

print(f"Tipo: {tipo}, Valor: {valor}")


# FORMATO DOS DADOS DE ENVIO NA SIMULAÇÃO (!!!)
dados_enviados_sensor = {
    "id": id_circuit,
    "device": 
    {
        "id": id_device,
        "tipo": tipo,
        "valor": valor,
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
