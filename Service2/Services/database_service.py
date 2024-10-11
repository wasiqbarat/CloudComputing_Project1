import mysql.connector

class Database():
    host = 'tai.liara.cloud'          
    port = 34424
    user = 'root'
    password = 'r03LTfZ5eZ4bDhZuBaZY6xYv'
    database = 'condescending_aryabhata'

    def query_liara_database(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )

            cursor = connection.cursor()
            
            query = f"SELECT * FROM Requests;"
            cursor.execute(query)

            results = cursor.fetchall()

            for row in results:
                print(row)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                
    def updateCaption(self, id, image_caption):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )

            cursor = connection.cursor()
            
            query = f"UPDATE Requests SET ImageCaption = '{image_caption}' WHERE id = {id}"
            cursor.execute(query)
            connection.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    
    def updateStatus(self, id, status):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )

            cursor = connection.cursor()
            
            query = f"UPDATE Requests SET status = '{status}' WHERE id = {id}"
            cursor.execute(query)
            connection.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                

if __name__ == "__main__":
    db = Database()
    #db.updateStatus(6, 'Rea')
    db.query_liara_database()
    #db.updateCaption(6, "this is a caption")
