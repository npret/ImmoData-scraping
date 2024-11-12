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