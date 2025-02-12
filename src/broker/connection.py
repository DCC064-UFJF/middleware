from pika import BlockingConnection, ConnectionParameters

connection = BlockingConnection(ConnectionParameters(host='my-rabbit', port=5672))
channel = connection.channel()