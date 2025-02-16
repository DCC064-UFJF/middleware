from flask import Blueprint, request

from bson import json_util

from json import loads

from http_server.services.actuator import get_actuators

actuator_blueprint = Blueprint('actuator', __name__)

@actuator_blueprint.route('', methods=['get'])
def get_all():
    """
    Retorna todos os atuadores de um circuito específico, sendo o último valor mais recente registrado deles (pega o último timestamp, isto é, o valor mais atualizado).
    """
    circuit_id = int(request.args.get('id'))

    # Passando os parâmetros para a função get_sensors
    return loads(json_util.dumps(get_actuators(circuit_id)))

"""Construir o código para o publisher ser em outro broker."""

