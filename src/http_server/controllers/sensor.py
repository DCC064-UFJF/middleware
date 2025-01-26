from http_server.services.sensor import get_sensors

from flask import Blueprint
from bson import json_util
from json import loads

sensor_blueprint = Blueprint('sensor', __name__)

@sensor_blueprint.route('/', methods=['GET'])
def get_all():
  return loads(json_util.dumps(get_sensors()))
