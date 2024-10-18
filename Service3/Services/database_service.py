import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")      
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

def updateImageURL(id, url):
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        cursor = connection.cursor()
            
        query = f"UPDATE Requests SET newImageURL = '{url}' WHERE id = {id}"
        cursor.execute(query)
        connection.commit()

        return "URL Updated!"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
            
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


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
    
#Returns all Requests with 'Ready' status  
def checkRequestsStatus():
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        cursor = connection.cursor()
            
        query = "SELECT * FROM Requests WHERE Status = 'Ready'"
        cursor.execute(query)
            
        results = cursor.fetchall()
        
        # for row in results:
        #     print(row)
        return results
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")



#returns email by id
def getEmail(id):
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        cursor = connection.cursor()
            
        query = f"SELECT * FROM Requests WHERE id = '{id}'"
        cursor.execute(query)
            
        results = cursor.fetchall()
            
        # for row in results:
        #     print(row)

        connection.close()
        return results
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
            
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# if __name__ == "__main__":
#     #db.checkRequestsStatus()
#     #db.updateCaption(6, "this is a caption")
#     #db.checkRequestsStatus()
    

