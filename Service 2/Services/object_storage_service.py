import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

class StorageService:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("LIARA_ENDPOINT"),
            aws_access_key_id=os.getenv("LIARA_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("LIARA_SECRET_KEY"),
        )
        self.bucket_name = os.getenv("LIARA_BUCKET_NAME")

    def upload_file(self, file, filename):
        try:
            self.s3.upload_fileobj(file, self.bucket_name, filename)
            return {"message": "File uploaded successfully."}
        except NoCredentialsError:
            return {"message": "Liara credentials not found."}
        except Exception as e:
            return {"message": str(e)}

    def download_file(self, filename):
        try:
            self.s3.download_file(self.bucket_name, filename, filename)
        except NoCredentialsError:
            return {"message": "Liara credentials not found."}
        except Exception as e:
            return {"message": str(e)}

    def list_files(self):
        try:
            files = self.s3.list_objects(Bucket=self.bucket_name)
            return [file["Key"] for file in files.get("Contents", [])]
        except NoCredentialsError:
            return {"message": "Liara credentials not found."}
        except Exception as e:
            return {"message": str(e)}
        
    

