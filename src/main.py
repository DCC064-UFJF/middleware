from os import getenv

from http_server.controllers.sensor import sensor_blueprint
from http_server.controllers.actuator import actuator_blueprint
from http_server.controllers.circuit import circuit_blueprint

from dotenv import load_dotenv
from flask import Flask

from utils import channel, connection

load_dotenv()

app: Flask = Flask(__name__)

app.register_blueprint(sensor_blueprint, url_prefix='/sensor')
app.register_blueprint(actuator_blueprint, url_prefix='/actuator')
app.register_blueprint(circuit_blueprint, url_prefix='/circuits')

@app.route('/')
def home():
    return "API de Sensores Rodando!"
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=getenv('FLASK_DEBUG', '1') == '1')

  connection.close()