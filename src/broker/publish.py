from pika import BasicProperties, DeliveryMode

from broker.connection import channel

publish(queue: str, message: str):
  channel.basic_publish(
    exchange='',
    routing_key=queue,
    body=message.encode(),
    properties=BasicProperties(delivery_mode=DeliveryMode.Persistent)
  )