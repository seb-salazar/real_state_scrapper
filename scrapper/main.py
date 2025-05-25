from utils import write_json_into_file, upload_folder_to_s3
from constants import *
from scrapper import Scrapper
from datetime import datetime

def main():
    print("started")

    # Base scrapper, to get all elements from each city (comune)
    scrapper = Scrapper(base_url="https://www.portalinmobiliario.com/venta/departamento")

    # for each city
    for city in cities:
        # Test initially with one city
        if city not in ("nunoa", "las-condes"): #("nunoa")
            continue

        # scrape and save all the data
        apartments_data = scrapper.get_global_data(city=city)
        for data in apartments_data:
            # write the csv files
            write_json_into_file(data=data,file_name=city)

    # upload to s3
    # get current date and time to create folder
    now = datetime.now()
    # Format as string (e.g., '2025-05-18')
    date_string = now.strftime("%Y-%m-%d")

    upload_folder_to_s3(
        local_folder='scrapper/data',
        bucket_name=BUCKET_NAME,
        s3_folder_prefix=f'scrapper/data/{date_string}'
    )

    print("done")

main()
