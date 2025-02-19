from http_server.services.circuit import get_all_circuits,get_devices_by_circuit,get_last_sensor_data,get_sensor_values_by_date,get_last_actuator_data

from flask import Blueprint, request,jsonify
from bson import json_util
from json import loads

circuit_blueprint = Blueprint('circuits', __name__)

# http://localhost:5000/circuits
@circuit_blueprint.route('', methods=['GET'])
def all():
    """
        Retorna um array com os ids dos circuitos existentes
    """
    return loads(json_util.dumps(get_all_circuits()))


# http://localhost:5000/circuits/1/devices
@circuit_blueprint.route('/<circuit_id>/devices', methods=['GET'])
def devices_by_circuit(circuit_id):
    """
        Retorna todos os dados de todos os SENSORES/ATUADORES de um determinado circuito
    """
    return loads(json_util.dumps(get_devices_by_circuit(circuit_id)))


# http://localhost:5000/circuits/3/sensor/2/last
@circuit_blueprint.route('/<circuit_id>/sensor/<sensor_id>/last', methods=['GET'])
def last_sensor_data(circuit_id, sensor_id):
    """
        Retorna o ultimo valor gravado de um SENSOR de um CIRCUITO
    """
    return loads(json_util.dumps(get_last_sensor_data(circuit_id, sensor_id)))


# http://localhost:5000/circuits/1/actuator/4/last
@circuit_blueprint.route('/<circuit_id>/actuator/<actuator_id>/last', methods=['GET'])
def last_actuator_data(circuit_id, actuator_id):
    """
        Retorna o ultimo valor gravado de um ATUADOR de um CIRCUITO
    """
    return loads(json_util.dumps(get_last_actuator_data(circuit_id, actuator_id)))


# http://localhost:5000/circuits/3/sensor/2/all?start_date=2025-01-01T00:00:00&end_date=2025-02-31T23:59:59
@circuit_blueprint.route('/<circuit_id>/sensor/<sensor_id>/all', methods=['GET'])
def sensor_values_by_date(circuit_id, sensor_id):
    """
        Retorna todos os dados de um SENSOR de um CIRCUITO dentro de um período específico
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    data = get_sensor_values_by_date(circuit_id, sensor_id, start_date, end_date)

    if not data:
        return jsonify({"message": "No data found", "start_date": start_date, "end_date": end_date}), 404

    return jsonify(data)