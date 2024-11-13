# Imports

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Functions

def get_cookies_from_website(url: str) -> dict[str, str]:
    """
    Function to get specific cookies from "immoweb.be"

    :param url: String containing immoweb link from where to obtain cookies.

    :return: Dictionary containing specified cookies.
    """

    driver = webdriver.Chrome()

    driver.get(url)
    time.sleep(10)  # Wait for the page to load and cookies to be set

    # Handle cookie consent banner
    shadow_host = driver.find_element(By.ID, 'usercentrics-root')
    shadow_root = shadow_host.shadow_root
    elem = shadow_root.find_element(By.CSS_SELECTOR, "button[data-testid='uc-accept-all-button']")
    elem.click()

    # Obtain cookies and close driver

    cookies = driver.get_cookies()
    driver.quit()

    # Format cookies for scraping using different package
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    keys = ['immoweb_session', 'XSRF-TOKEN', '__cf_bm']
    final_cookies = {key: cookies_dict[key] for key in keys}

    return final_cookies

def get_url_list(url: str) -> list[str]:
    """
    Function to obtain a list of URLs to scrape from given immoweb listings page.

    :param url: String containing immoweb URL to obtain listing URLs from.

    :return: List of URLs
    """

    url_list = []
    counter = 0

    driver = webdriver.Chrome()

    driver.get(url)
    time.sleep(10)  # Wait for the page to load and cookies to be set

    # Handle cookie consent banner
    shadow_host = driver.find_element(By.ID, 'usercentrics-root')
    shadow_root = shadow_host.shadow_root
    elem = shadow_root.find_element(By.CSS_SELECTOR, "button[data-testid='uc-accept-all-button']")
    elem.click()

    # Get URLs 
    while len(url_list) < 62:

        # Find all elements of search page results
        listings = driver.find_elements(By.CSS_SELECTOR, "li[class='search-results__item']")

        # Collect all links within these elements (should be one per listing)

        for listing in listings:
            link_elements = listing.find_elements(By.TAG_NAME, 'a')
            for link in link_elements:
                href = link.get_attribute('href')
                if href:  # Check if href is not None
                    url_list.append(href)
                else:
                    print(f"not found link {link}")
        
        # Go to next page

        next_page = driver.find_elements(By.CSS_SELECTOR, "a[class='pagination__link pagination__link--next button button--text button--size-small']")
        href = next_page[0].get_attribute('href')
        print(f"scraped page {counter + 1}")
        counter += 1
        driver.get(href)
        time.sleep(10)

    # Return list of URLs  
    #return url_list

    # Save URLs to file

    with open('links.txt', 'w') as f:
        for link in url_list:
            f.write(link+f"\n")
                                 
if __name__ == "__main__":
    url = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&page=1&orderBy=relevance'
    #cookies = get_cookies_from_website(url)
    #print(cookies)  # You can save this to a file or pass it to the Scrapy spider
    #url_list = get_url_list(url)
    #print(url_list)
    #print(len(url_list))
    get_url_list(url)
    