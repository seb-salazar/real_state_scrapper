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

    # Get the absolute path to the scrapper directory
    scrapper_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(scrapper_dir, "data", date_string)

    # Check if the directory exists
    if not os.path.exists(data_dir):
        # If it doesn't exist, create it
        os.makedirs(data_dir)

    # Serializing json
    json_object = json.dumps(data)
    
    file_path = os.path.join(data_dir, f"{file_name}.json")

    # Writing to sample.json
    with open(file_path, "w") as outfile:
        outfile.write(json_object)
        outfile.write('\n')
    
    return data_dir  # Return the directory path for reference

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

    # Ensure local_folder is absolute path
    local_folder = os.path.abspath(local_folder)
    
    if not os.path.exists(local_folder):
        print(f"❌ Error: Folder {local_folder} does not exist")
        return

    for root, _, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            # Get the relative path from the base folder
            relative_path = os.path.relpath(local_path, local_folder)
            s3_key = os.path.join(s3_folder_prefix, relative_path).replace("\\", "/")

            try:
                s3.upload_file(local_path, bucket_name, s3_key)
                print(f"✅ Uploaded {local_path} to s3://{bucket_name}/{s3_key}")
            except Exception as e:
                print(f"❌ Error uploading {local_path}: {str(e)}")
