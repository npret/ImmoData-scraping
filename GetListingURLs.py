import requests
from requests import Session
from bs4 import BeautifulSoup
from HelperFunctions import get_soup
from multiprocessing import Pool, get_context
from time import perf_counter

def get_url_list(page_number: int,
                  headers: dict[str:str] = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',} ,
                  session: Session = requests.Session()) -> list[str]:

    url_list = []

    base_url = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&page={page_number}&orderBy=relevance'
    
    try:
        soup = get_soup(base_url, headers, session, page_number)

        listings = soup.find_all("div", attrs={"class": "card--result__body"})
        
        for listing in listings:
            for link in listing.find_all("a", attrs={"class": "card__title-link"}):
                href = link.get("href")
                if href:
                        url_list.append(href)
                else:
                        print(f"not found link {link}")

    except Exception as e:
        print(f"Error occurred on page {page_number + 1}: {e}")

    return url_list

def quick_get_urls(num_pages:int) -> list[str]:
    ctx = get_context("spawn")
    with ctx.Pool(processes=10) as pool:
        results = pool.map(get_url_list, range(1, num_pages + 1))

    url_list = []
    for page_urls in results:
        url_list.extend(page_urls)

    with open('url.txt', 'w') as f:
         for url in url_list:
              f.write(url +"\n")

    print(len(url_list))
    return url_list



if __name__ == "__main__":

    number_pages = 333
    start_time_multi = perf_counter()

    list = quick_get_urls(number_pages)
    print(f"\nTime spent inside the multi loop: {perf_counter() - start_time_multi} seconds.")  

    print(len(list))
 