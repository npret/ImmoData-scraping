import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


def get_cookies_from_website(url: str) -> dict[str, str]:
    """
    Function to get specific cookies from "immoweb.be"

    :param url: String containing immoweb link from where to obtain cookies.

    :return: Dictionary containing specified cookies.
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
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

# Set up the URL and headers
#url = 'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/gent/9000/20314083'
#url = 'https://www.immoweb.be/en/classified/apartment/for-sale/saint-gilles/1060/20306773'
# URL with a fireplace:
url = 'https://www.immoweb.be/en/classified/house/for-sale/wetteren/9230/20316344'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

# Use the get_cookies_from_website function to retrieve cookies
cookies = get_cookies_from_website(url)

# Make the request with the obtained cookies
session = requests.Session()
session.cookies.update(cookies)
response = session.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')


def parse_listing(soup):    

    # Get locality as 4-digit postal code - NOT WORKING
    """
    locality = None
    address_rows = soup.select('span.classified__information--address-row')
    print(f"Found {len(address_rows)} address rows.")

    for row in address_rows:
        text = row.get_text(strip=True)
        print("Extracted text:", text)
    
        locality_match = re.search(r'\b\d{4}\b', text)
        if locality_match:
            locality = locality_match.group()
            print("Found postal code:", locality)
            break
    """


    # Select the custom tag iw-classified-address
    address_container = soup.find('iw-classified-address', class_='classified__information--address')

    # Debugging: Print the address container to verify it's found
    print("Address Container:", address_container)

    locality = None  # Initialize locality to None

    # Ensure address_container is not None before proceeding
    if address_container is not None:
    # Check for children of the address container
        children = address_container.find_all(recursive=False)
        print("Children:", children)

    # Iterate through children to find text content
        for child in children:
        # Concatenate all contents within each child
            text = ''.join(str(content) for content in child.contents).strip()
            print("Child Text:", text)

        # Extract postal code by searching for a numerical part
            postal_code_match = re.search(r'\b\d{4,5}\b', text)
        
            if postal_code_match:
                locality = postal_code_match.group()
                print("Postal Code:", locality)
                break
        else:
            print("Postal code not found in any child elements.")
    else:
        print("Address container not found.")

    # get property type - need strategy
    property_type = None

    # Get property subtype - need strategy
    property_subtype = None

    # Get price - need to clean ',', '€' and figure out how to deal with ranges.
    price = None
    price_element = soup.find('p', class_='classified__price')
    if price_element:
        price_span = price_element.find('span', {'aria-hidden': 'true'})
        if price_span:
            price = price_span.get_text(strip=True)

    # Get type of slae - excl. Life sales - need strategy
    sale_type = None

    #Get number of rooms - need to figure out how to deal with ranges.
    rooms_number = None
    rooms_number_text = soup.find('span', class_='overview__text', string=re.compile(r'\d+\s*bedrooms?', re.IGNORECASE))
    if rooms_number_text:
        rooms_number = ' - '.join(re.findall(r'\d+', rooms_number_text.get_text(strip=True)))

    # Get the living area number - need to figure out how to deal with ranges.
    living_area = None
    for span in soup.find_all('span', class_='overview__text'):
        abbreviation_span = span.find('span', class_='abbreviation')
        if abbreviation_span and 'm²' in abbreviation_span.get_text():
            abbreviation_span.extract()
        
            living_area_text = re.findall(r'\d+', span.get_text(strip=True))
        
            if living_area_text:
                living_area = ' - '.join(living_area_text)
            break

    # Get bin value for if kitchen is equipped or not
    kitchen_th = soup.find('th', string="Kitchen type")
    if kitchen_th:
        kitchen_td = kitchen_th.find_next_sibling('td')
        if kitchen_td:
            kitchen_type = ''.join(str(content) for content in kitchen_td.contents).strip().lower()
    
        # Determine if the kitchen is equipped
            is_kitchen_equipped = 1 if kitchen_type in ["installed", "hyper equipped"] else 0
        else:
            is_kitchen_equipped = None
    else:
        is_kitchen_equipped = None
    furnished_th = soup.find('th', string="Furnished")

    # Get bin value for if furnished or not.
    is_furnished = None

    if furnished_th:
        furnished_td = furnished_th.find_next_sibling('td')
        if furnished_td:
            furnished_status = ''.join(str(content) for content in furnished_td.contents).strip().lower()
            print("Processed furnished status:", furnished_status)
        
            is_furnished = 1 if furnished_status == "yes" else 0
        else:
            is_furnished = None
    else:
        is_furnished = None

    fireplace_th = soup.find('th', string="How many fireplaces?")

    # Get bin value for fireplace.
    is_open_fire = None 

    if fireplace_th:
        fireplace_td = fireplace_th.find_next_sibling('td')
        if fireplace_td:
            fireplace_count_text = ''.join(str(content) for content in fireplace_td.contents).strip()
        
            if fireplace_count_text.isdigit() and int(fireplace_count_text) > 0:
                is_open_fire = 1
            else:
                is_open_fire = 0
    else:
        is_open_fire = None
    
    # Get bin value for terrace + terrace area
    terrace_th = soup.find('th', string="Terrace surface")

    is_terrace = None
    terrace_area = None  

    if terrace_th:
        terrace_td = terrace_th.find_next_sibling('td')
        if terrace_td:
            terrace_text = ''.join(str(content) for content in terrace_td.contents).strip()        
            terrace_text = re.sub(r'\D', '', terrace_text)
        
            is_terrace = 1 if terrace_text else 0
        
            if terrace_text.isdigit():
                terrace_area = int(terrace_text)
    else:
        is_terrace = 0
        terrace_area = None

    #Get in value if garden + garden area
    garden_th = soup.find('th', string="Garden surface")

    is_garden = None
    garden_area = None 

    if garden_th:
        garden_td = garden_th.find_next_sibling('td')
        if garden_td:
            garden_text = ''.join(str(content) for content in garden_td.contents).strip()
        
            garden_text = re.sub(r'\D', '', garden_text)  # Remove any non-digit characters
        
            is_garden = 1 if garden_text else 0
        
            if garden_text.isdigit():
                garden_area = int(garden_text)
    else:
        is_garden = 0
        garden_area = None

    return {
        "locality": locality,
        #"type of property": property_type,
        #"subtype of property": property_subtype,
        "price": price,
        #"type of sale": sale_type,
        "number of rooms": rooms_number,
        "living area": living_area,
        "fully equipped kitchen": is_kitchen_equipped,
        "furnished": is_furnished,
        "open fire": is_open_fire,
        "terrace": is_terrace,
        "terrace area": terrace_area,
        "garden": is_garden,
        "garden area": garden_area,
        #"surface of the land": surface_of_land,
        #"surface area of the plot of land": surface_area_of_land,
        #"number of facades": facades_number,
        #"swimming pool": is_pool,
        #"state of the building": building_state
    }

result = parse_listing(soup)
print(result)