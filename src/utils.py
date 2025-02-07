from database.connection import mongo_client


# Função para inserir dados no banco.
def insert_db(data):
    return mongo_client.sensor.data.insert_one(data)