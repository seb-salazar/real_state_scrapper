from utils import write_json_into_file, upload_folder_to_s3
from constants import *
from scrapper import Scrapper
import os

def main():
    print("started")

    # Base scrapper, to get all elements from each city (comune)
    scrapper = Scrapper(base_url=os.environ['SCRAPPING_MAIN_URL'])

    # Get the absolute path to the scrapper directory
    scrapper_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(scrapper_dir, "data")

    # for each city
    for city in cities:
        # Test initially with one city
        # if city not in ("nunoa", "las-condes", "vitacura"): #("nunoa")
        #    continue

        # scrape and save all the data
        apartments_data = scrapper.get_global_data(city=city)
        for data in apartments_data:
            # write the csv files
            write_json_into_file(data=data, file_name=city)

    # upload to s3
    upload_folder_to_s3(
        local_folder=data_dir,
        bucket_name=os.environ['BUCKET_NAME'],
        s3_folder_prefix='scrapper/data'
    )

    print("done")

main()
