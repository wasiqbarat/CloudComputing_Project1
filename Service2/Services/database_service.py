import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")      
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

def updateStatus(id, status):
    try:
        connection = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
        )

        cursor = connection.cursor()
            
        query = f"UPDATE Requests SET status = '{status}' WHERE id = {id}"
        cursor.execute(query)
        connection.commit()

        connection.close()
        return "Status Updated!"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
            
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def updateCaption(id, caption):
    try:
        connection = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
        )

        cursor = connection.cursor()
            
        query = f"UPDATE Requests SET ImageCaption = '{caption}' WHERE id = {id}"
        cursor.execute(query)
        connection.commit()

        connection.close()
        return "caption Updated!"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
            
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


    

