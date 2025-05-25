import boto3
import json
import os
from datetime import datetime

def write_json_into_file(data: dict, file_name: str = "example") -> str:
    if not data:
        return None

    # Get current date and time
    now = datetime.now()
    # Format as string (e.g., '2025-05-18')
    date_string = now.strftime("%Y-%m-%d")

    directory = f"./data/{date_string}"

    # Check if the directory exists
    if not os.path.exists(directory):
        # If it doesn't exist, create it
        os.makedirs(directory)

    # Serializing json
    json_object = json.dumps(data)
    
    file_path = f"{directory}/{file_name}.json"

    # Writing to sample.json
    with open(file_path, "w") as outfile:
        outfile.write(json_object)
        outfile.write('\n')
    
    return file_path

def upload_to_s3(file_path, bucket_name, object_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ.get('AWS_REGION', 'us-east-2')
    )
    s3.upload_file(file_path, bucket_name, object_key)
    print(f"✅ Uploaded {file_path} to s3://{bucket_name}/{object_key}")
