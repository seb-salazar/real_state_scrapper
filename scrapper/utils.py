import boto3
import json
import os
from datetime import datetime

def write_json_into_file(data: dict, file_name: str = "example"):
    if not data:
        return None

    # get current date and time to create folder
    now = datetime.now()
    # Format as string (e.g., '2025-05-18')
    date_string = now.strftime("%Y-%m-%d")

    # Check if the directory exists
    if not os.path.exists(f"./data/{date_string}"):
        # If it doesn't exist, create it
        os.makedirs(f"./data/{date_string}")

    # Serializing json
    json_object = json.dumps(data)
    
    file_path = f"./data/{date_string}/{file_name}.json"

    # Writing to sample.json
    with open(file_path, "w") as outfile:
        outfile.write(json_object)
        outfile.write('\n')

def upload_file_to_s3(file_path, bucket_name, object_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ.get('AWS_REGION', 'us-east-2')
    )
    s3.upload_file(file_path, bucket_name, object_key)
    print(f"✅ Uploaded {file_path} to s3://{bucket_name}/{object_key}")

def upload_folder_to_s3(local_folder, bucket_name, s3_folder_prefix):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ.get('AWS_REGION', 'us-east-2')
    )

    for root, _, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_folder)
            s3_key = os.path.join(s3_folder_prefix, relative_path).replace("\\", "/")  # Use S3-compatible paths

            s3.upload_file(local_path, bucket_name, s3_key)
            print(f"✅ Uploaded {local_path} to s3://{bucket_name}/{s3_key}")
