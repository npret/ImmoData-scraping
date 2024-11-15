# Imports

import requests
from requests import Session
from bs4 import BeautifulSoup

# Functions

def get_soup(url: str, headers: dict[str:str], session: Session, page_number: int):
    """
    Simple function to execute get request, parse html and return Beautifulsoup object.

    : param url: str: String containing URL to get.
    : param headers: dict: Dict containing User agent specification for the get request.
    : param session: requests.Session(): Requests Session() object.
    : param page_number: int: Integer representing which page number is being contacted.

    : return: Beautifulsoup object containing parsed html.
    """
    response = session.get(url, headers= headers)
    if page_number != None:
        print(f"Request for page {page_number} - response : {response.status_code}")
    else:
        print(f"Solving compound listing - Getting individual url - response : {response.status_code}")
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    return soup