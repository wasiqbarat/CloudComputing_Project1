import pika
from dotenv import load_dotenv
import os

load_dotenv()

parametres = pika.URLParameters(os.getenv('RABBITMQ_URL'))
connection = pika.BlockingConnection(parametres)
channel = connection.channel()

def send_to_rabbitMQ(num):
    channel.queue_declare(queue='requests_queue')
    channel.basic_publish(exchange='', routing_key='requests_queue', body=str(num))

def receive_content_of_rabbitMQ():
    channel.queue_declare(queue='requests_queue')

    def callback(ch, method, properties, body):
        print(int(body))
    # Start consuming messages
    channel.basic_consume(queue='requests_queue', on_message_callback=callback, auto_ack=True)

    print("Waiting for messages. To exit, press CTRL+C")
    channel.start_consuming()

    connection.close()




