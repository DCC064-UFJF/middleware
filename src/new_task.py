#!/usr/bin/env python
import pika
import sys
from datetime import datetime
import json
import random

# realiza conexão
connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host='my-rabbit'))
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declara uma filac chamada "task_queue"
channel.queue_declare(queue='task_queue', durable=True)

types = ["Temperatura", "Umidade", "Pressão", "atuador"]
id_circuit = random.randint(1, 4)
id_device = random.randint(1, 6)
tipo = random.choice(types)

if tipo == "atuador":
    valor = random.randint(0, 1)
else:
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
