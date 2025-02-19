from collections import defaultdict
from database.connection import mongo_client
from datetime import datetime, timedelta


def get_sensors(id_circuito: int, interval_seconds: int):
    db = mongo_client['application']
    collection = db['sensores']
    
    now = datetime.now()
    start_time = now - timedelta(seconds=interval_seconds)

    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S') 
    end_time_str = now.strftime('%Y-%m-%dT%H:%M:%S')

    sensors = collection.find({
        'circuito_id': id_circuito,
        'timestamp': {'$gte': start_time_str, '$lte': end_time_str}
    })


    sensor_values = defaultdict(list)
    sensor_timestamps = defaultdict(list)
    
    for sensor in sensors:
        sensor_values[sensor['id']].append(sensor['valor'])
        sensor_timestamps[sensor['id']].append(sensor['timestamp'])

    # Construindo o resultado final
    result = []
    for sensor_id, _ in sensor_values.items():
        result.append({
            'id': sensor_id,
            'values': sensor_values[sensor_id],
            'timestamps': sensor_timestamps[sensor_id]
        })

    return result


""""
ROTAS:

/circuitos => { id_circuito: string }[]
/circuitos/<id_circuito>/devices => { tudo do device }[]
/circuitos/<id_circuito>/devices/<id_device> => { tudo do device (dnv)  }


CIRCUITO_ID, SENSOR_ID, DATA_INICIO, DATA_FIM => ARRAY COM OS REGISTROS NO INTERVALO DE DATAS PASSADO


CIRCUITO_ID, ATUADOR_ID => ULTIMO VALOR REGISTRADO (VALOR ATUAL)

CIRCUITO_ID, ATUADOR_ID, NOVO_VALOR => CONFIGURA NOVO VALOR DO ATUADOR (POST) 

"""
