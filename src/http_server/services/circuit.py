from collections import defaultdict
from database.connection import mongo_client
from datetime import datetime, timedelta

def get_all_circuits():
    db = mongo_client['application']
    collection = db['circuitos']

    circuits = collection.find()

    return [circuit["id"] for circuit in circuits]

def get_devices_by_circuit(circuit_id: int):
    db = mongo_client['application']
    collection_sensores = db['sensores']
    collection_atuadores = db['atuadores']

    sensors = collection_sensores.find({"circuito_id": int(circuit_id)})
    atuadores = collection_atuadores.find({"circuito_id": int(circuit_id)})

    devices_list = []
    for sensor in sensors:
        timestamp = sensor.get("timestamp", datetime.utcnow())

        # Se timestamp já for string, usa direto; senão, converte para ISO 8601
        if isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()

        devices_list.append({
            "circuito_id": sensor.get("circuito_id"),
            "id": sensor.get("id"),
            "timestamp": timestamp,
            "tipo": sensor.get("tipo", "Desconhecido"),
            "valor": sensor.get("valor", 0)
        })
    
    for atuador in atuadores:
        timestamp = atuador.get("timestamp", datetime.utcnow())

        # Se timestamp já for string, usa direto; senão, converte para ISO 8601
        if isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()

        devices_list.append({
            "circuito_id": atuador.get("circuito_id"),
            "id": atuador.get("id"),        
            "valor": atuador.get("valor", 0),
            "timestamp": timestamp,
        })

    return devices_list

def get_last_sensor_data(circuit_id: int, sensor_id: int):
    db = mongo_client['application']
    collection = db['sensores']

    last_device = collection.find_one(
        {"circuito_id": int(circuit_id), "id": int(sensor_id)}        
    )

    if not last_device:
        return {}  

    timestamp = last_device.get("timestamp", datetime.utcnow())
    if isinstance(timestamp, datetime):
        timestamp = timestamp.isoformat()

    return {
        "id": last_device.get("id"),
        "tipo": last_device.get("tipo", "Desconhecido"),
        "valor": last_device.get("valor", 0),
        "timestamp": timestamp,
        "circuito_id": last_device.get("circuito_id")
    }

def get_last_actuator_data(circuit_id: int, actuator_id: int):
    db = mongo_client['application']
    collection = db['atuadores']

    last_device = collection.find_one(
        {"circuito_id": int(circuit_id), "id": int(actuator_id)}        
    )

    if not last_device:
        return {}  

    timestamp = last_device.get("timestamp", datetime.utcnow())
    if isinstance(timestamp, datetime):
        timestamp = timestamp.isoformat()

    return {
        "id": last_device.get("id"),
        "valor": last_device.get("valor", 0),
        "timestamp": timestamp,
        "circuito_id": last_device.get("circuito_id")
    }

def get_sensor_values_by_date(circuit_id: int, device_id: int, start_date: str, end_date: str):
    db = mongo_client['application']
    collection = db['sensores']

    # Criar o filtro de consulta
    query = {"circuito_id": int(circuit_id), "id": int(device_id)}

    # Adiciona filtro de data, se fornecido
    if start_date and end_date:
        query["timestamp"] = {}
        if start_date:
            query["timestamp"]["$gte"] = start_date
        if end_date:
            query["timestamp"]["$lte"] = end_date

    # Buscar registros no intervalo e ordenar por timestamp crescente
    devices = collection.find(query).sort("timestamp", 1)

    # Converter documentos para lista de dicionários formatados
    device_list = []
    for device in devices:
        timestamp = device.get("timestamp")

        # Converter timestamp para string ISO 8601, se necessário
        if isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()

        device_list.append({
            "id": device.get("id"),
            "tipo": device.get("tipo", "Desconhecido"),
            "valor": device.get("valor", 0),
            "timestamp": timestamp,
            "circuito_id": device.get("circuito_id")
        })

    return device_list

""""
ROTAS:

/circuitos => { id_circuito: string }[]
/circuitos/<id_circuito>/devices => { tudo do device }[]
/circuitos/<id_circuito>/devices/<id_device> => { tudo do device (dnv)  }


CIRCUITO_ID, SENSOR_ID, DATA_INICIO, DATA_FIM => ARRAY COM OS REGISTROS NO INTERVALO DE DATAS PASSADO


CIRCUITO_ID, ATUADOR_ID => ULTIMO VALOR REGISTRADO (VALOR ATUAL)

CIRCUITO_ID, ATUADOR_ID, NOVO_VALOR => CONFIGURA NOVO VALOR DO ATUADOR (POST) 

"""
