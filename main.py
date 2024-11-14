# Imports

from GetListingURLs import get_url_list, quick_get_urls
from GetListingDetails import get_dict_from_url
from CreateDataFrame import parse_listing_info
from requests import Session
import pandas as pd

# Main script

if __name__ == "__main__":

    # Define headers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',} 
    number_pages = 333
    session = requests.Session()
    # Get listing URLs
    quick_get_urls(number_pages, headers, session)

    #get_url_list(headers, session)

    # Get listings details, only relevant info

    #relevant_info_dicts = 

    # Parse to pd.DataFrame
    df = parse_listing_info(relevant_info_dicts)
    df.to_csv('ImmowebScrapingResult.csv')


# Get URLs

base_url = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false'
total_pages = 10

page_numbers = list(range(1, total_pages + 1))

with Pool(processes=4) as pool:
    results = pool.starmap(get_urls, [(base_url, page) for page in page_numbers])

all_urls = [url for page_urls in results for url in page_urls]



#import requests
#from bs4 import BeautifulSoup

#url = 'https://www.immoweb.be/en/classified/apartment/for-sale/boom/2850/20310616'

#session = requests.Session()
#headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}                   
#session.cookies.update(cookies)

#try_request = session.get(url, headers= headers)
#print(try_request.status_code)
#html = try_request.content



