# Imports

import requests
from requests import Session
from bs4 import BeautifulSoup

# Functions

def get_soup(url: str, headers: dict[str:str], session: Session, page_number: int):
    response = session.get(url, headers= headers)
    if page_number != None:
        print(f"Request for page {page_number} - response : {response.status_code}")
    else:
        print(f"Solving compound listing - Getting individual url")
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    return soup