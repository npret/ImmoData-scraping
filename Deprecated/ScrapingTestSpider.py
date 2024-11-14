link_list = ['https://www.immoweb.be/en/classified/apartment/for-sale/antwerpen/2100/20315980',
             'https://www.immoweb.be/en/classified/apartment/for-sale/hoboken/2660/20315431',
             'https://www.immoweb.be/en/classified/apartment/for-sale/uccle/1180/20315652',
             'https://www.immoweb.be/en/classified/apartment/for-sale/antwerpen/2018/20315324',
             'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/anderlecht/1070/20313048',
             'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/helecine/1357/20315407',
             'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/gent/9000/20314083',
             'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/sint-denijs-westrem/9051/20315271',
             'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/forest/1190/20315731',
             'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/chaumont-gistoux/1325/20315432',
             'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/asse/1730/20315766']

# Imports

import requests
from bs4 import BeautifulSoup
import pandas as pd
from Deprecated.SeleniumFunctions import get_cookies_from_website
import re


def get_soup(url, headers, session):
    response = session.get(url, headers= headers)
    print(f"Obtained response from {response.url} with status {response.status_code}")
    content = response.content
    soup = BeautifulSoup(content, 'html')
    return soup

def get_empty_data():
    data = {'locality':None,
            'property_type':None,
            'property_subtype':None,
            'price':None,
            'sale_type':None,
            'rooms':None,
            'area_living':None,
            'equipped_kitchen':None,
            'furnished':None,
            'fire':None,
            'terrace':None,
            'terrace_area':None,
            'garden':None,
            'garden_area':None,
            'land_surface':None,
            'plot_surface':None,
            'number_facade':None,
            'swimming_pool':None,
            'building_state':None,
            'immoweb_code': None}
    
    return data

def fill_data(soup):
    data = get_empty_data()

    code = soup.find_all("div", attrs={"class": "classified__header--immoweb-code"})[0].text
    code = find_number(code)
    data['immoweb_code'] = code
    
def find_number(string):

    num_reg = r"\d+"

    return re.findall(num_reg, string)[0]


    # Get the synopsis section
for elem in soup.find_all("section", attrs={"id": "synopsis-details"}):
    # Get the text of the synopsis
    for elem2 in elem.find_all("div", attrs={"class":"content-txt"}):
        # Just like that
        print(elem2.text)

def scrape_immoweb(url_list):

    data = []
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    cookies = get_cookies_from_website('https://www.immoweb.be')
    #cookies = {'immoweb_session' : 'eyJpdiI6IjVubHc4Q1R3RlpvRXkwaVVWQkdNZ3c9PSIsInZhbHVlIjoiakZGMjViTnVxTmROYm1GU2ZYUU9XR3NLMjJrTG84cmVkYm1NN2tqSWhCWjFHQjJQNmxHdDBZbnhPS1JsdzBzSmtUdmpWOXhOdllaeTdqRWZhZ0k4cWhwQWw5MGVwZVlZVTlDQ0ZWcHNJR3h6aXZEdFNMZVg3UTVnR0tGWHcyK1UiLCJtYWMiOiIxZDg1ZjRhNTkxODlkM2VhN2Y3MzY2NTdmMDRkYTc5NjAzYzY5YWVkNDAyYTFjMDEzMmQ3ZmI1MGYyYWY4MjBlIn0%3D',
                       #'XSRF-TOKEN': 'eyJpdiI6IkxwRzIwZFEzMTg5VzJDYWtvWi8zM3c9PSIsInZhbHVlIjoiNERVU1NhdlEzVzBIbkZ4cmV4Z2JMbHN3NjVrRWZUMzg0OWd1MVd3N1E3ckI5aGhIRVlaa2czWnl4QVdvbjJUSTZxMkhGdlA1ZzA1c0xxU1A0N0hlaS8rZnV4TmxldDVIbHNUZDVNNCtpSS9qb2x3enNodFFITFJGTlZEZVVrN2siLCJtYWMiOiI2MTJmZDcxNzkyM2YwMTM1ZjZkZGRjZTM5YjIzMGFmNTNiNDA1NTAyMmE0OWRhMTBlMzQwMDVjZjY3YmMzNmE3In0%3D',
                       #'__cf_bm' : 'MoKFFUtnsCnBMVsc_XiGba.KtzFY_Ta1f6UtGsI_7j4-1731414232-1.0.1.1-0sQuyt.MEHq3govqH2hn5G0QTGypm5VhAs_Bbhx8a1jvPdIz6yUY5HZKXWDlbV8WF2w.FVvnEgBOUdzQ46C3Rw'}

    session = requests.Session()
    session.cookies.update(cookies)

    for url in url_list:
        if 'new-real-estate' in url:
            data.append(get_empty_data())
        else:
            soup = get_soup(url, headers, session)
            data.append(fill_data(soup))



if __name__ == "__main__":

    link = link_list[0]
    result_dict = scrape_immoweb(link)
    print(result_dict)
