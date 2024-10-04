from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy

class DatabaseService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create_requests_table(self):
        # Check if the table already exists
        table_exists_query = text("""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME = 'Requests'
        """)
    
        result = self.db.session.execute(table_exists_query).scalar()
    
        # If table exists, return message
        if result > 0:
            return "Table already exists"
        
        # Create the table if it does not exist
        create_table_query = text("""
        CREATE TABLE IF NOT EXISTS Requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(120) NOT NULL UNIQUE,
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

    def insert_request(self, email, status, image_caption, new_image_url):
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
        return f"Request from {email} inserted successfully."
    
    
    def get_request_by_id(self, request_id):
        select_query = text("SELECT * FROM Requests WHERE id = :request_id")
        result = self.db.session.execute(select_query, {'request_id': request_id})
        request = result.fetchone() 
        #The fetchone() method is typically used when you expect a single record to be returned 
        # (e.g., when querying by a unique identifier like id).
        
        if request:
            return dict(request)
        else:
            return None
        
    