from os import getenv

from dotenv import load_dotenv

load_dotenv()

env = {
  'mongo_url': getenv('MONGO_URL', 'mongodb://localhost:27017/'),
  'flask_debug': True if getenv('FLASK_DEBUG', '1') == '1' else False
}