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
    
    for sensor in sensors:
        sensor_values[sensor['id']].append(sensor['valor'])

    # Construindo o resultado final
    result = []
    for sensor_id, values in sensor_values.items():
        result.append({
            'id': sensor_id,
            'values': values
        })

    return result

