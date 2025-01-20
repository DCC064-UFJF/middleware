import pika
import os
import sys

def main():
    # realização da conexão com o broker
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # cria a fila hello (boa prática criar a fila novamente)
    channel.queue_declare(queue='hello')

    # para receber mensagens, é necessário subescrever um callback na fila. Tal callback será chamado pela própria biblioteca.
    def callback(ch, method, properties, body):
        print(f"[x] received {body}")
        
    channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)

    # loop infinito para ficar esperando pelos dados.
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)