from database.connection import mongo_client

def get_sensors():
  sensors = mongo_client.sensor.data.find()
  return list(sensors)
