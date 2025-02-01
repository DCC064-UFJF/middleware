# python 3.11

import random

from paho.mqtt import client as mqtt_client


broker = 'localhost' # ip do broker
port = 1883
topic = "python/mqtt"
client_id = f'subscribe-{random.randint(0, 100)}'  # gera um id de subscriber aleatório.
# nome e senha dos usuários do RabbitMQ
print("My client id is: ", client_id)
username = 'guest'
password = 'guest'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # client = mqtt_client.Client(client_id)
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Cria a função callback chamada toda vez que o cliente recebe mensagens do broker MQTT.
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
