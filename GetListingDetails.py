# Imports

import requests
from requests import Session
from bs4 import BeautifulSoup
import json
import re
from HelperFunctions import get_soup
from multiprocessing import get_context, cpu_count, Pool
from GetListingURLs import quick_get_urls, get_url_list
from time import perf_counter

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


def read_parse_listings(url_list: list[str],
                        index_range,
                        headers: dict[str:str] = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',},
                        session: Session = requests.Session()) -> list[dict]:

    result = []
    individual_urls = []

    for line_number in index_range:
        url = url_list[line_number].strip()

        listing_dict = get_dict_from_url(url, headers, session, line_number)

        if is_compound_sale(listing_dict):
            print(f"Solving compound listing for {url}")
            soup = get_soup(url, headers, session, None)
            individual_listings = get_compound_sale_urls(soup)
            for listing_url in individual_listings:
                individual_urls.append(listing_url)
                individual_dict = get_dict_from_url(listing_url, headers, session, None)
                result.append(individual_dict)

        else:
            individual_urls.append(url)
            result.append(listing_dict)

    return result, individual_urls

def quick_parse(url_list: list[str], num_processes: int = None) -> list[dict]:

    if num_processes is None:
        num_processes = cpu_count()  # Use the number of available CPUs by default
    
    url_index_ranges = [range(i, len(url_list), num_processes) for i in range(num_processes)]
    
    listing_dicts = []
    individual_urls = []

    with get_context('spawn').Pool(processes=num_processes) as pool:
        results = pool.starmap(read_parse_listings, [(url_list, url_index_range) for url_index_range in url_index_ranges])

        for result, urls in results:
            listing_dicts.extend(result)
            individual_urls.extend(urls)

    with open('url_individual.txt', 'w') as file:
        for url in individual_urls:
            file.write(url + "\n")

    return listing_dicts


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

def get_compound_sale_urls(soup: BeautifulSoup) -> list[str]:
    individual_urls = []
    
    # Find all tags that include the text 'apartment'
    tags_with_text = soup.find_all(string=lambda text: "apartment" in text.lower())
    
    # Check each tag for a parent with the class 'grid'
    for tag in tags_with_text:
        # Find the closest parent 'div' with class 'grid'
        grid = tag.find_parent('div', class_='grid')
        if grid:
            # Now, check for subtitles and extract valid links
            subtitles = grid.find_all('span', class_='text-block__subtitle')
            
            # We already know this grid contains an "apartment" mention
            links = grid.find_all('a', href=True)
            valid_links = [link['href'] for link in links if link['href'].startswith("https://www.immoweb.be/en/classified/")]

            # Extend individual_urls with valid links if found
            if valid_links:
                individual_urls.extend(valid_links)
                # Optionally print each found URL
                #for valid_link in valid_links:
                    #print(f"Found URL: {valid_link}")

    return individual_urls


if __name__ == "__main__":

    number_pages = 10
    start_time_multi = perf_counter()

    list = quick_get_urls(number_pages)
    dicts = quick_parse(list)
    print(len(dicts))
    print(dicts[0])
    print(dicts[100])
    print(f"\nTime spent inside the multi loop: {perf_counter() - start_time_multi} seconds.")  
