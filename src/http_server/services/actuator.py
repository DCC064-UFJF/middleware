from database.connection import mongo_client
from datetime import datetime, timedelta


def get_actuators(id_circuito: int):
    db = mongo_client['application']
    collection = db['atuadores']

    atuadores = collection.find({
        'circuito_id': id_circuito,
    }).sort('timestamp', -1) 

    recent_atuadores = {}
    for atuador in atuadores:
        atuador_id = atuador['id']
        if atuador_id not in recent_atuadores:
            recent_atuadores[atuador_id] = atuador

    return list(recent_atuadores.values())

