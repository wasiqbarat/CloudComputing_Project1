import requests
import json

API_URL = "https://api-inference.huggingface.co/models/kothariyashhh/GenAi-Texttoimage"
headers = {"Authorization": "Bearer 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"}

def call_api(text):
    response = requests.post(API_URL, headers=headers, json=text)
    image_bytes = response.content
    return image_bytes

#text = json.dumps({"inputs":"Elon musk in afghanistan!"})
#image_bytes = call_api(text)
