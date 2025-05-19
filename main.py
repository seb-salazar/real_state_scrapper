from utils import write_json_into_file
from constants import cities
from scrapper import Scrapper

def main():
    print("started")
    scrapper = Scrapper(base_url="https://www.portalinmobiliario.com/venta/departamento")

    # for each city
    for city in cities:
        # Test initially with one city
        if city != "nunoa":
            continue

        # scrape and save all the data
        apartments_data = scrapper.get_global_data(city=city)
        for data in apartments_data:
            write_json_into_file(data=data,file_name=city)

    print("done")

main()
