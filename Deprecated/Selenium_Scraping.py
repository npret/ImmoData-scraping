# Imports

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Open driver and navigate to page

url = "https://www.immoweb.be/en"

driver = webdriver.Firefox()
driver.get(url)

# Get cookie GDPR button and click

cookies = driver.find_element(By.XPATH, "//button[@data-testid='uc-accept-all-button']") # Get gdpr button link
cookies.click()

# Navigate to the search list, choose houses and apartments, deselect life annuity

search_page = driver.find_element(By.XPATH, "//button[@id='searchBoxSubmitButton']")
search_page.click()

search_advanced = driver.find_element(By.XPATH, "//span[@id='buttonMoreFilter']")
search_advanced.click()




# Close driver

driver.close()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
options = Options()
options.add_argument('--headless')  # Run in headless mode if needed
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service('C:/Program Files/Google/Chrome/Application/chrome.exe')  # Replace with your chromedriver path
driver = webdriver.Chrome(service=service, options=options)

# Open the website
driver.get('https://www.immoweb.be')

# Wait for the page to load and cookies to be set
time.sleep(5)

### HANDLE COOKIE CONSENT BANNER

# Get cookies from the driver and format them for `requests`
cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}

# Close the browser
driver.quit()

# Print or use the cookies in your `requests` call
print(cookies)