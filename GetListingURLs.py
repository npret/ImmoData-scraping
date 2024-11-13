import requests

def get_url_list():

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    url_list = []

    for page_number in range(333):
        base_url = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&page={page_number + 1}&orderBy=relevance'
        response = requests.get(base_url, headers= headers)
        print(f"Request for page {page_number + 1} - response : {response.status_code}")
        content = response.content
        soup = BeautifulSoup(content, 'html')

        listings = soup.find_all("div", attrs={"class": "card--result__body"})
        
        for listing in listings:
            for link in listing.find_all("a"):
                href = link.get("href")
                if href:
                        url_list.append(href)
                else:
                        print(f"not found link {link}")

    return url_list