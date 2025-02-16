import json
from flask import Blueprint, jsonify, request

from bson import json_util

from json import loads

from http_server.services.actuator import get_actuators

import pika
from utils import channel, connection

actuator_blueprint = Blueprint('actuator', __name__)

@actuator_blueprint.route('', methods=['get'])
def get_all():
    """
    Retorna todos os atuadores de um circuito específico, sendo o último valor mais recente registrado deles (pega o último timestamp, isto é, o valor mais atualizado).
    """
    circuit_id = int(request.args.get('id'))

    # Passando os parâmetros para a função get_sensors
    return loads(json_util.dumps(get_actuators(circuit_id)))

#suba junto o worker_actuator.py
# http://localhost:5000/actuator/sendtask?id_circuito=3&id_sensor=2&new_value=0
@actuator_blueprint.route('sendtask', methods=['get'])
def send_task():
    """
    Alterar essa rota para POST depois...
    Ao enviar uma requisição post, com o parâmetro new_value, envia o new_value para o broker
    """
    id_circuito = request.args.get('id_circuito')
    id_sensor = request.args.get('id_sensor')
    new_value = request.args.get('new_value')

    msg = {
        'id_circuito': id_circuito,
        'id_sensor': id_sensor,
        'new_value': new_value
    }

    message = json.dumps(msg).encode()

    channel.basic_publish(
        exchange='',
        routing_key='actuators',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
    ))

    return jsonify({"message": "Operacao realizada com sucesso!"}), 200

