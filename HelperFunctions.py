# Imports

import requests
from requests import Session
from bs4 import BeautifulSoup

# Functions

def get_soup(url: str, headers: dict[str:str], session: Session, page_number: int) -> Beautifulsoup:
    response = session.get(url, headers= headers)
    print(f"Request for page {page_number + 1} - response : {response.status_code}")
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    return soup