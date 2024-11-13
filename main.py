# Imports

from SeleniumFunctions import get_cookies_from_website, get_url_list
from SeleniumPat import get_urls
from multiprocessing import Pool

# Get cookies

#url = 'https://www.immoweb.be'
#cookies = get_cookies_from_website(url)

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



