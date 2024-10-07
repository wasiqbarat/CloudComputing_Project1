import re #regix
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from Services.object_storage_service import StorageService
from Services.database_service import DatabaseService
import json

app = Flask(__name__)

# Configuring SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql://root:r03LTfZ5eZ4bDhZuBaZY6xYv@tai.liara.cloud:34424/condescending_aryabhata"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
datebase = DatabaseService(db)
object_storage = StorageService()


@app.route('/rabbitmq', methods=['GET'])
def rabbitMQ_test():
    #message = rabbitMQ.receiveMessage("test_queue")
    message = "HIIIIIIII"
    return message

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    else:
        return False

@app.route('/db' , methods=['GET'])
def dbtest():
    response = datebase.get_request_by_id(4)
    print(response)
    return jsonify(f"{response}")

@app.route('/request', methods=['POST'])
def sendRequest():
    if 'file' not in request.files:
        return "Please Provide an Image!"    
    
    email = request.form['email']
    if not is_valid_email(email):
        return "Your Email is Invalid!"

    file = request.files['file']

    if file.filename == '':
        return "NO selected file"

    if file:
        response = datebase.insert_request(email, "pending")
        print(response)
        
        if "ID" in response:
            id = response["ID"]
            object_storage.upload_file(file, f"{id}.jpg")
            
            return f"Request from {email} inserted successfully with ID: {id}"
        else:
            return "Failed to insert the request."
    
    else:
        return "Unsuccessfully"
    


@app.route('/status/<id>', methods=['GET'])
def getRequestId(id):
    req_args = request.view_args


if __name__ == '__main__':
    app.run(port=5002, debug=True)

