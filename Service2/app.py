import pika
import requests
import os
from dotenv import load_dotenv
from Services import object_storage_service
from Services.database_service import Database

load_dotenv()

def receive_content_of_rabbitMQ():
    parametres = pika.URLParameters(os.getenv('RABBITMQ_URL'))
    connection = pika.BlockingConnection(parametres)
    channel = connection.channel()

    def callback(ch, method, properties, body):
        id = int(body)
        print(int(body), "The id received from RabbitMQ")
        image_to_text_API(id)

    # Start consuming messages
    channel.basic_consume(queue='requests_queue', on_message_callback=callback, auto_ack=True)

    print("Waiting for messages")
    channel.start_consuming()


def image_to_text_API(id):
        object_storage_service.download_file(f"{id}.jpg")

        API_URL = os.getenv('TEXT_TO_IMAGE_API_URL')
        headers = {"Authorization": f"Bearer {os.getenv('TEXT_TO_IMAGE_API_TOKEN')}"}

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

