from os import getenv

from http_server.controllers.sensor import sensor_blueprint

from dotenv import load_dotenv

from flask import Flask

load_dotenv()

app: Flask = Flask(__name__)

app.register_blueprint(sensor_blueprint, url_prefix='/sensor')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=getenv('FLASK_DEBUG', '1') == '1')