import json
import os


def write_json_into_file(data: dict, file_name: str = "example", directory: str = "./data"):
    if not data:
        return None

    # Check if the directory exists
    if not os.path.exists(directory):
        # If it doesn't exist, create it
        os.makedirs(directory)

    # Serializing json
    json_object = json.dumps(data)

    # Writing to sample.json
    with open(f"{directory}/{file_name}.json", "a") as outfile:
        outfile.write(json_object)
        outfile.write('\n')
