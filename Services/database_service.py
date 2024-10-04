from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
import json

class DatabaseService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create_requests_table(self):
        create_table_query = text("""
        CREATE TABLE IF NOT EXISTS Requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(120) NOT NULL,
            status VARCHAR(20) NOT NULL,
            ImageCaption VARCHAR(255),
            newImageURL VARCHAR(255)
        )
        """)
    
        self.db.session.execute(create_table_query)
        self.db.session.commit()
    
        return "Table created successfully"


    def remove_requests_table(self):
        remove_table_query = text("DROP TABLE IF EXISTS Requests;")
        self.db.session.execute(remove_table_query)
        self.db.session.commit()
        return "Requests table removed."

    def show_tables(self):
        result = self.db.session.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        return tables

    def insert_request(self, email, status, image_caption=None, new_image_url=None):
        insert_query = text("""
            INSERT INTO Requests (email, status, ImageCaption, newImageURL)
            VALUES (:email, :status, :image_caption, :new_image_url)
        """)

        self.db.session.execute(insert_query, {
            'email': email,
            'status': status,
            'image_caption': image_caption,
            'new_image_url': new_image_url
        })
        self.db.session.commit()

        # Fetch the last inserted ID using MySQL's LAST_INSERT_ID() function
        result = self.db.session.execute(text("SELECT LAST_INSERT_ID()"))
        id = result.scalar()  # Fetch the single scalar result (the last inserted ID)
        
        return {"ID" : id}
    
    
    def get_request_by_id(self, request_id):
        select_query = text("SELECT * FROM Requests WHERE id = :request_id")
        result = self.db.session.execute(select_query, {'request_id': request_id})
        request = result.fetchone() 
        #The fetchone() method is typically used when you expect a single record to be returned 
        # (e.g., when querying by a unique identifier like id).
        
        if request:
            return request
        else:
            return None
        

    