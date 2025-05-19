import json
import os
from datetime import datetime

def write_json_into_file(data: dict, file_name: str = "example"):
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

    # Writing to sample.json
    with open(f"{directory}/{file_name}.json", "w") as outfile:
        outfile.write(json_object)
        outfile.write('\n')
