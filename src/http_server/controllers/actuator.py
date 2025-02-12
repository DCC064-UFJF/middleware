from http_server.services.actuator import send_request

from flask import Blueprint

actuator_blueprint = Blueprint('actuator', __name__)

@actuator_blueprint.route('/', methods=['POST'])
def send_request():
    return send_request(request.json)
