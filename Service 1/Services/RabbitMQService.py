import pika

class RabbitMQ:
    def __init__(self, URL):
        self.URL = URL
    
    def getConnection(self):
        parametres = pika.URLParameters(self.URL)
        connection = pika.BlockingConnection(parametres)
        return connection
    
    def sendMessage(self, queueName, message):
        connection = self.getConnection()
        channel = connection.channel()

        channel.queue_declare(queue=queueName)
        channel.basic_publish(exchange='', routing_key=queueName, body=message)
        connection.close()

    
    def receiveMessage(self, queueName):
        connection = self.getConnection()
        channel = connection.channel()

        method_frame, header_frame, body = channel.basic_get(queue=queueName)

        if method_frame:
            channel.basic_ack(method_frame.delivery_tag)
            message = body.decode('utf-8')
        else:
            message = None

        connection.close()
        
        return message
    
    