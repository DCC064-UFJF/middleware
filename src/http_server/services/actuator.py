from broker.publish import publish

def send_request(data):
    publish('actuator', data)
    