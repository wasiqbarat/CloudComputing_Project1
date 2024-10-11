import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv('TEXT_TO_IMAGE_API_URL')
headers = {"Authorization": f"Bearer {os.getenv('TEXT_TO_IMAGE_API_TOKEN')}"}

def call_api(text):
    response = requests.post(API_URL, headers=headers, json=text)
    image_bytes = response.content
    return image_bytes

#text = json.dumps({"inputs":"Elon musk in afghanistan!"})
#image_bytes = call_api(text)
