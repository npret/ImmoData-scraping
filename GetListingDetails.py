# Imports

import requests
from requests import Session
from bs4 import BeautifulSoup
import json
import re
from HelperFunctions import get_soup

# Functions

def get_dict_from_url(url: str, headers: dict[str:str], session: Session) -> dict:

    soup = get_soup(url, headers, session, None)

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

    with open('url.txt', 'r') as file:
        for line in file:
            url = file.readline().strip()

            listing_dict = get_dict_from_url(url, headers)

            if is_compound_sale(listing_dict):
                print(f"Solving compound listing for {url}")
                soup = get_soup(url, headers, session, None)
                individual_listings = get_compound_sale_urls(soup, listing_dict)
                # Remove compound listing url
                for listing_url in individual_listings:
                    # append individual listing url
                    individual_dict = get_dict_from_url(listing_url, headers)
                    result.append(individual_dict)

            else:
                result.append(listing_dict)

    return result

def get_relevant_info(list_dicts_listings: list[dict]) -> list[dict]:
    
    # List will contain dictionaries for each listing containing relevant info
    relevant_info_list = []
    
    # Iterate over each listing in the main dictionary.
    for listing in list_dicts_listings:
        
        locality = None
        locality = listing.get('property', {}).get('location', {}).get('postalCode')

        property_type = None
        property_type = listing.get('property', {}).get('type')

        property_subtype = None
        property_subtype = listing.get('property', {}).get('subtype')

        price = None
        price = listing.get('transaction', {}).get('sale', {}).get('price')

        sale_type = None
        sale_type = listing.get('price', {}).get('type')

        rooms = None
        rooms = listing.get('property', {}).get('bedroomCount')

        living_area = None
        living_area = listing.get('property', {}).get('netHabitableSurface')

        # Need to make sure what the different status posibilies are
        is_kitchen_equipped = None
        kitchen_equipped_status = listing.get('property', {}).get('kitchen', {}).get('type')
        if kitchen_equipped_status is not None and kitchen_equipped_status != "None" and kitchen_equipped_status != "":
            kitchen_equipped_status = kitchen_equipped_status.lower()
            if kitchen_equipped_status == "installed":
                is_kitchen_equipped = 1
            else:
                is_kitchen_equipped = 0

        # Need to double check status possibilities
        is_furnished = None
        furnished_status = listing.get('transaction', {}).get('sale', {}).get('isFurnished')
        if furnished_status is not None and furnished_status != "None" and furnished_status != "":
            furnished_status = furnished_status.lower()
            if furnished_status == "yes":
                is_furnished = 1
            else:
                is_furnished = 0

        is_fireplace = None
        fireplace_status = listing.get('property', {}).get('fireplaceExists')
        if fireplace_status is not None and fireplace_status != "None" and fireplace_status != "":
            if fireplace_status == True:
                is_fireplace = 1
            else:
                is_fireplace = 0

        is_terrace = None
        terrace_status = listing.get('property', {}).get('hasTerrace')
        if terrace_status is not None and terrace_status != "None" and terrace_status != "":
            if terrace_status == True:
                is_terrace = 1
            else: 
                is_terrace = 0

        terrace_area = None
        terrace_area = listing.get('property', {}).get('terraceSurface')

        is_garden = None
        garden_status = listing.get('property', {}).get('hasGarden')
        if garden_status is not None and garden_status != "None" and garden_status != "":
            if garden_status == True:
                is_garden = 1
            else:
                is_garden = 0

        garden_area = None
        garden_area = listing.get('property', {}).get('gardenSurface')

        # Garden area twice??
        surface_land = None
        surface_land = listing.get('property', {}).get('gardenSurface')

        #surface_land + living area
        surface_area_plot = None

        def safe_convert(value):
        # Check if the value is a number and not string 'None' or empty
            if value and value != 'None':
                try:
                    return float(value)  # convert to float
                except ValueError:
                    return None  # Return None if can't be converted
            return None  # Return None if value is 'None' or None

        # Convert living_area and surface_land safely for math reasons
        living_area = safe_convert(living_area)
        surface_land = safe_convert(surface_land)

        # Calculate surface_area_plot
        if living_area is not None and surface_land is not None:
            surface_area_plot = living_area + surface_land
        elif living_area is None and surface_land is not None:
            surface_area_plot = surface_land
        elif living_area is not None and surface_land is None:
            surface_area_plot = living_area

        facades = None
        facades = listing.get('property', {}).get('building', {}).get('facadeCount')

        is_pool = None
        pool_status = listing.get('property', {}).get('hasSwimmingPool')
        if pool_status is not None and pool_status != "None" and pool_status != "":
            if pool_status == True:
                is_pool = 1
            else:
                is_pool = 0

        building_state = None
        building_state = listing.get('property', {}).get('building', {}).get('condition')
        
        #Extract info from listings into a dictionary
        relevant_info = {'Locality': locality,
                         'Type of property': property_type,
                         'Subtype of property': property_subtype,
                         'Price': price,
                         'Type of sale': sale_type,
                         'Number of rooms': rooms,
                         'Living Area': living_area,
                         'Fully equipped kitchen': is_kitchen_equipped,
                         'Furnished': is_furnished,
                         'Fireplace': is_fireplace,
                         'Terrace': is_terrace,
                         'Terrace area': terrace_area,
                         'Garden': is_garden,
                         'Garden area': garden_area,
                         'Surface of the land': surface_land,
                         'Surface area of the plot of land': surface_area_plot,
                         'Number of facades': facades,
                         'Swimming pool': is_pool,
                         'State of the building': building_state
                        }

        # Add dictionary for listing to our list.
        relevant_info_list.append(relevant_info)

    return relevant_info_list
    
# Load mock data for testing get_relevant_info()
with open('mock_data.json', 'r') as file:
    mock_data = json.load(file)

if isinstance(mock_data, dict):
    mock_data = [mock_data]

test_result = get_relevant_info(mock_data)
print(test_result)

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
