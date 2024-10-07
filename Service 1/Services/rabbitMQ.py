import pika


credentials = pika.PlainCredentials('smgwtkdg', 'Y8AXDjrQNmSewjQS_5ZFzqKral6c1UKd')
#parameters = pika.ConnectionParameters('cougar-01.rmq.cloudamqp.com', 5672, 'smgwtkdg', credentials)
#connection = pika.BlockingConnection(parameters)


parametres = pika.URLParameters("amqps://smgwtkdg:Y8AXDjrQNmSewjQS_5ZFzqKral6c1UKd@hummingbird.rmq.cloudamqp.com/smgwtkdg")
connection = pika.BlockingConnection(parametres)
channel = connection.channel()

def send_to_rabbitMQ(num):
    channel.queue_declare(queue='requests_queue')
    channel.basic_publish(exchange='', routing_key='requests_queue', body=str(num))
    # connection.close()

def receive_content_of_rabbitMQ():
    channel.queue_declare(queue='requests_queue')

    def callback(ch, method, properties, body):
        print(int(body))
    # Start consuming messages
    channel.basic_consume(queue='requests_queue', on_message_callback=callback, auto_ack=True)

    print("Waiting for messages. To exit, press CTRL+C")
    channel.start_consuming()

    connection.close()


send_to_rabbitMQ(4)


