# python 3.11

import random
import time

from paho.mqtt import client as mqtt_client


broker = 'localhost' # ip do broker
port = 1883
topic = "python/mqtt"
client_id = f'publish-{random.randint(0, 1000)}' # gera um id de cliente aleatório.
# nome e senha dos usuários do RabbitMQ
username = 'guest'
password = 'guest'

def connect_mqtt():
    # função callback para para informar o status de conexão com o broker. 
    def on_connect(client, userdata, flags, rc, *args):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# Loop que envia mensagens a cada segundo para o tópico "/python/mqtt" e sai do loop após 10 mensagens.
def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 10:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
