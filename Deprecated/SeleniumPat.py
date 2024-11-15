# Imports

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool

# Function for getting URLs

def get_urls(base_url, page_number):
    driver = webdriver.Chrome()
    
    all_urls = []
    
    try:     
        url = f"{base_url}&page={page_number}"
        driver.get(url)
        # wait for the page to load
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return typeof UC_UI !== 'undefined'")
        )

        # deny all consents
        driver.execute_script('UC_UI.denyAllConsents().then(UC_UI.closeCMP);')

        

            # parse the page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract search item URLs
        li_items = soup.find_all('li', class_='search-results__item')
        for li_item in li_items:
            article = li_item.find('article')
            if article:
                link_tag = article.find('a', class_='card__title-link')
                if link_tag and 'href' in link_tag.attrs:
                    all_urls.append(link_tag['href'])


        # Check if there is a next page link
    

    except Exception as e:
        print("An error occurred on page {page_number}:", e)

    finally:
        driver.quit()

    return all_urls