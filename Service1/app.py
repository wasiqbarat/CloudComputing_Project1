import re #regix
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from Services import object_storage_service
from Services.database_service import DatabaseService
from Services import rabbitMQ

app = Flask(__name__)

# Configuring SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql://root:r03LTfZ5eZ4bDhZuBaZY6xYv@tai.liara.cloud:34424/condescending_aryabhata"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
datebase = DatabaseService(db)


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    else:
        return False
    

@app.route('/newrequest', methods=['POST'])
def newRequest():
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
            object_storage_service.upload_file(file, f"{id}.jpg")

            rabbitMQ.send_to_rabbitMQ(id)  #send ID to rabbitMQ
            
            return f"Request from {email} inserted successfully with ID: {id}"
        else:
            return "Failed to insert the request."
    
    else:
        return "Unsuccessfully"
    

@app.route('/status/<id>', methods=['GET'])
def getRequestId(id):    
    request_status = datebase.get_request_by_id(id)
    if request_status[2] == 'done':
        return f"{request_status[4]}"
    else:
        return "under review..."
 
if __name__ == '__main__':
    app.run(port=5000, debug=True)


