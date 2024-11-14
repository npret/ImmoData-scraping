import requests
from requests import Session
from bs4 import BeautifulSoup
from HelperFunctions import get_soup
from multiprocessing import Pool, getcontext

def get_url_list(num_pages: int, headers: dict[str:str], session: Session) -> list[str]:

    url_list = []

    with open('url.txt', 'w') as f:
        for page_number in range(num_pages):
            base_url = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&page={page_number + 1}&orderBy=relevance'
            
            try:
                soup = get_soup(base_url, headers, session, page_number)

                listings = soup.find_all("div", attrs={"class": "card--result__body"})
                
                for listing in listings:
                    for link in listing.find_all("a", attrs={"class": "card__title-link"}):
                        href = link.get("href")
                        if href:
                                url_list.append(href)
                                f.write(href +"\n")
                        else:
                                print(f"not found link {link}")

            except Exception as e:
                print(f"Error occurred on page {page_number + 1}: {e}")

    return url_list

def quick_get_urls(num_pages:int, headers: dict[str:str], session: Session) -> list[str]:
    ctx = get_context("fork")
    with ctx.Pool(processes=10) as pool:
        results = pool.starmap(get_url_list, [(num_pages, headers, session)])

    url_list = []
    for page_urls in results:
        url_list.extend(page_urls)

    print(len(url_list))
    return url_list



if __name__ == "__main__":
     list = get_url_list()
     print(list)
     print(len(list))