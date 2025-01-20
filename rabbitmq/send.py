import pika

# realização da conexão com o broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# cria a fila para recepção das mensagens
channel.queue_declare(queue='hello')

# uma mensagem nunca pode ser enviada diretamente pra fila. Ela precisa primeiro passar por um 'exchange', que nesse caso é o padrão ''.
channel.basic_publish(exchange='', routing_key='hello', body='Hello, World!')
print("[x] Sent 'Hello, World!'")

connection.close()