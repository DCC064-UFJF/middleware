from http_server.services.sensor import get_sensors

from flask import Blueprint, request
from bson import json_util
from json import loads

sensor_blueprint = Blueprint('sensor', __name__)

@sensor_blueprint.route('/', methods=['GET'])
def get_all():
    sensor_id = int(request.args.get('id'))
    intervalo = int(request.args.get('intervalo'))

    # Passando os parâmetros para a função get_sensors
    return loads(json_util.dumps(get_sensors(sensor_id, intervalo)))