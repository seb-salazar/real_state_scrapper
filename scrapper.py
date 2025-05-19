import requests
import time
from constants import *
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse, parse_qs

# As a starting point, assume the "From" values
class Scrapper:
    city: str

    def __init__(self, base_url: str):
        self.base_url = base_url


    def build_paginated_url(self, page: int) -> str:
        if page == 1:
            return f"{self.base_url}/{self.city}-metropolitana/{ONLY_PROYECTS_URL_FLAG}"
        else:
            return f"{self.base_url}/{self.city}-metropolitana/_Desde_{(page - 1) * 50 + 1}{ONLY_PROYECTS_URL_FLAG}"


    def get_global_data(self, city: str):
        self.city = city
        keep_going = True
        page = 1
        global_data = []

        while keep_going:
            try:
                url = self.build_paginated_url(page)
                print(f"City: {self.city}, Page: {page}, URL: {url}")

                page_data = self.get_page_data(url)
                global_data.append(page_data)
                page += 1

            except requests.exceptions.HTTPError as http_error:
                if http_error.response.status_code == 404:
                    keep_going = False

        return global_data



    def get_page_data(self, url: str) -> list:
        data = []

        response = requests.get(url, timeout=None)
        response.raise_for_status()
        
        try:
            data = self._parse_and_get_items(response)
            if not data:
                time.sleep(3)
                print(f"trying AGAIN for city: {self.city}")
                data = self.get_page_data(url)

        except AttributeError:
            time.sleep(3)
            print(f"trying AGAIN for city: {self.city}")
            data = self.get_page_data(url)

        print(f"SUCCESS for city: {self.city}")
        return data


    def _parse_and_get_items(self, response: requests.Response) -> list:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all property cards
        property_cards = soup.find_all('div', class_=APARTMENT_RESULT_GRID_ELEMENT)

        # Extracted data will be stored here
        data_list = []

        for card in property_cards:
            property_data = {
                'property_url': '',
                'property_tracking_id': '',
                'property_title': '',
                'currency': '',
                'from_price': '',
                'dorms': '',
                'bathrooms': '',
                'gross_area': '',
                'location_name': '',
                'possession_date': '',
                'available_units': '',
                'property_sale_type': ''
            }

            # property_url and title
            title_tag = card.find('a', class_='poly-component__title')
            if title_tag:
                href = title_tag.get('href', '').strip()
                property_data['property_url'] = href
                property_data['property_title'] = title_tag.text.strip()

                # Extract tracking_id from URL fragment
                parsed = urlparse(href)
                if parsed.fragment:
                    tracking_params = parse_qs(parsed.fragment)
                    tracking_id = tracking_params.get('tracking_id', [''])[0]
                    property_data['property_tracking_id'] = tracking_id

            # Price
            currency_tag = card.find('span', class_='andes-money-amount__currency-symbol')
            fraction_tag = card.find('span', class_='andes-money-amount__fraction')
            if currency_tag:
                property_data['currency'] = currency_tag.text.strip()
            if fraction_tag:
                property_data['from_price'] = fraction_tag.text.strip()

            # Attributes list
            attributes = card.find_all('li', class_='poly-attributes_list__item')
            for attr in attributes:
                text = attr.text.strip().lower()
                if 'dormitorio' in text:
                    property_data['dorms'] = attr.text.strip()
                elif 'baño' in text:
                    property_data['bathrooms'] = attr.text.strip()
                elif 'útiles' in text:
                    property_data['gross_area'] = attr.text.strip()

            # Location
            location_tag = card.find('span', class_='poly-component__location')
            if location_tag:
                property_data['location_name'] = location_tag.text.strip()

            # Possession Date
            possession_tag = card.find('span', class_='poly-component__possession-date')
            if possession_tag:
                property_data['possession_date'] = possession_tag.text.strip()

            # Available Units
            units_tag = card.find('span', class_='poly-component__available-units')
            if units_tag:
                property_data['available_units'] = units_tag.text.strip()

            # Sale Type
            pill_tag = card.find('span', class_='poly-pill__pill')
            if pill_tag and 'PROYECTO' in pill_tag.text.upper():
                property_data['property_sale_type'] = 'PROYECTO'

            data_list.append(property_data)

        return data_list
