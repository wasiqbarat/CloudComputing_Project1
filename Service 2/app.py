import pika
import requests
from Services.object_storage_service import StorageService
from Services.database_service import Database

def receive_content_of_rabbitMQ():
    parametres = pika.URLParameters("amqps://smgwtkdg:Y8AXDjrQNmSewjQS_5ZFzqKral6c1UKd@hummingbird.rmq.cloudamqp.com/smgwtkdg")
    connection = pika.BlockingConnection(parametres)
    channel = connection.channel()

    def callback(ch, method, properties, body):
        id = int(body)
        print(int(body), "received content of rabbit mq")
        image_to_text_API(id)

    # Start consuming messages
    channel.basic_consume(queue='requests_queue', on_message_callback=callback, auto_ack=True)

    print("Waiting for messages")
    channel.start_consuming()


def image_to_text_API(id):
        object_storage = StorageService()
        object_storage.download_file(f"{id}.jpg")

        API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
        headers = {"Authorization": "Bearer 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"}

        with open(f"{id}.jpg", "rb") as f:
            data = f.read()
            
        response = requests.post(API_URL, headers=headers, data=data)
        caption = response.json()[0]['generated_text']

        db = Database()
        db.updateCaption(id, caption)
        db.updateStatus(id, 'Ready')
        print("Success")



receive_content_of_rabbitMQ()    
print('Keyboard Interrupted')

