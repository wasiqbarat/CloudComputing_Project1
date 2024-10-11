import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

s3 = boto3.client(
        "s3",
            endpoint_url=os.getenv("LIARA_ENDPOINT"),
            aws_access_key_id=os.getenv("LIARA_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("LIARA_SECRET_KEY"),
        )
bucket_name = os.getenv("LIARA_BUCKET_NAME")

def upload_file(file, filename):
    try:
        s3.upload_fileobj(file, bucket_name, filename)
        return {"message": "File uploaded successfully."}
    except NoCredentialsError:
        return {"message": "Liara credentials not found."}
    except Exception as e:
        return {"message": str(e)}

def download_file(filename):
    try:
        s3.download_file(bucket_name, filename, filename)
    except NoCredentialsError:
        return {"message": "Liara credentials not found."}
    except Exception as e:
        return {"message": str(e)}

def list_files():
    try:
        files = s3.list_objects(Bucket=bucket_name)
        return [file["Key"] for file in files.get("Contents", [])]
    except NoCredentialsError:
        return {"message": "Liara credentials not found."}
    except Exception as e:
        return {"message": str(e)}

def generate_presigned_url(filename):
    try:
        pre_signed_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": filename},
            ExpiresIn=12 * 60 * 60,  # 12 hours
        )
        return {"message": pre_signed_url}
    except NoCredentialsError:
        return {"message": "Liara credentials not found."}
    except Exception as e:
        return {"message": str(e)}

def generate_permanent_url(filename):
    try:
        filename_encoded = quote(filename)
        permanent_url = f"https://{bucket_name}.{os.getenv('LIARA_ENDPOINT').replace('https://', '')}/{filename_encoded}"
        return {"message": permanent_url}
    except NoCredentialsError:
        return {"message": "Liara credentials not found."}
    except Exception as e:
        return {"message": str(e)}
        
