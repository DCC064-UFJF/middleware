from database.connection import mongo_client
from datetime import datetime, timedelta


def get_sensors(id_circuito: int, interval_seconds: int):
    """
    Retorna todos os sensores de um circuito específico, no intervalo de tempo especificado.
    """
    db = mongo_client['application']
    collection = db['sensores']
    
    now = datetime.now()
    start_time = now - timedelta(seconds=interval_seconds)

    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S')  # Formato ISO 8601
    end_time_str = now.strftime('%Y-%m-%dT%H:%M:%S')

    # Certificando-se de que os timestamps sejam corretamente comparados com os objetos datetime
    sensors = collection.find({
        'circuito_id': id_circuito,
        'timestamp': {'$gte': start_time_str, '$lte': end_time_str}
    })

    return list(sensors)

