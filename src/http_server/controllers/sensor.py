from http_server.services.sensor import get_sensors

from flask import Blueprint, request
from bson import json_util
from json import loads

sensor_blueprint = Blueprint('sensor', __name__)

# localhost:5000/sensor?id=1&intervalo=30
@sensor_blueprint.route('', methods=['GET'])
def get_all():
    """
    Retorna todos os valores dos sensores de um circuito específico, no intervalo de tempo especificado.
    'id': id do sensor
    'values: array com os valores naquele intervalo de tempo.
    """
    circuit_id = int(request.args.get('id'))
    intervalo = int(request.args.get('intervalo'))

    # Passando os parâmetros para a função get_sensors
    return loads(json_util.dumps(get_sensors(circuit_id, intervalo)))