# Imports

import requests
from requests import Session
from bs4 import BeautifulSoup
import json
import re
from HelperFunctions import get_soup

# Functions

def get_dict_from_url(url: str, headers: dict[str:str], session: Session, line_number: int) -> dict:

    soup = get_soup(url, headers, session, line_number)

    # Parse the content to find the <script> tag containing "window.classified"
    script_tag = soup.find('script', string=re.compile(r'window\.classified\s*='))

    if script_tag:
        print(f"Got script_tag for {url}")
        # Extract the JSON part from the script content
        match = re.search(r'window\.classified\s*=\s*(\{.*?\});', script_tag.string)
        if match:
            classified_data = match.group(1)
            # Parse the JSON data
            classified_dict = json.loads(classified_data)

            return classified_dict

        else:
            print(f"JSON data not found within the script tag for {url}.")
    else:
        print(f"Script tag with 'window.classified' not found for {url}.")

def read_parse_listings(url_file_path: str, headers: dict[str:str], session: Session) -> list[dict]:

    result = []
    compound_urls = []
    individual_urls = []

    with open(url_file_path, 'r') as file:
        for line_number, line in enumerate(file, start= 1):
            url = line.strip()

            listing_dict = get_dict_from_url(url, headers, session, line_number)

            if is_compound_sale(listing_dict):
                print(f"Solving compound listing for {url}")
                compound_urls.append(url + "\n")
                soup = get_soup(url, headers, session, None)
                individual_listings = get_compound_sale_urls(soup, listing_dict)
                for listing_url in individual_listings:
                    individual_urls.append(listing_url + "\n")
                    individual_dict = get_dict_from_url(listing_url, headers, session, None)
                    result.append(individual_dict)

            else:
                result.append(listing_dict)

    with open(url_file_path, "r") as f:
        lines = f.readlines()
    with open(url_file_path, "w") as f:
        for line in lines:
            if line not in compound_urls:
                f.write(line)
    with open(url_file_path, "a") as f:
        for line in individual_urls:
            f.write(line)

    return result

def get_relevant_info(list_dicts_listings: list[dict]) -> list[dict]:
    for listing in list_dicts_listings:
        pass
    #write relevant code to extract the particular information needed from the listing dicts
    #place into new dict containing only relevant information
    #def get_empty_data():
    #data = {'locality':None,
     #       'property_type':None,
      #      'property_subtype':None,
       #     'price':None,
        #    'sale_type':None,
        #    'rooms':None,
        #    'area_living':None,
        #    'equipped_kitchen':None,
        #    'furnished':None,
        #    'fire':None,
        #    'terrace':None,
        #    'terrace_area':None,
        #    'garden':None,
        #    'garden_area':None,
        #    'land_surface':None,
        #    'plot_surface':None,
        #    'number_facade':None,
        #    'swimming_pool':None,
        #    'building_state':None,
        #    'immoweb_code': None}
    
    #return data

def is_compound_sale(classified_dict: dict) -> bool:
    return classified_dict['cluster'] != None

def get_compound_sale_urls(soup, compound_dict: dict) -> list[str]:
    ...
    # Write function to get URLs of individual listings on the compound sale using the soup
    # also pass the dict created ; look at 'cluster', is units : [{type:commercial, ...}, {type:apartment, ..., items:[{id:xxxxx}]}]
    # use id numbers and if sold information to search all a tags where href contains the id number
    # concat all urls to list
