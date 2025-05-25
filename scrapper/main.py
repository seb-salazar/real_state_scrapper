from utils import write_json_into_file, upload_to_s3
from constants import *
from scrapper import Scrapper

def main():
    print("started")

    # Base scrapper, to get all elements from each city (comune)
    scrapper = Scrapper(base_url="https://www.portalinmobiliario.com/venta/departamento")

    # for each city
    for city in cities:
        # Test initially with one city
        if city not in ("nunoa"): #("nunoa", "las-condes")
            continue

        # scrape and save all the data
        apartments_data = scrapper.get_global_data(city=city)
        for data in apartments_data:
            # write the csv file
            file_path = write_json_into_file(data=data,file_name=city)
            # upload to s3
            upload_to_s3(file_path=file_path, bucket_name=BUCKET_NAME, object_key=f'scrapper/{file_path}')

    print("done")

main()
