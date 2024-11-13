import requests
from bs4 import BeautifulSoup
import json
import re

# Assuming you already have the HTML content from requests.get() stored in a variable `html_content`
# soup = BeautifulSoup(html_content, 'html.parser')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
url = 'https://www.immoweb.be/en/classified/apartment/for-sale/antwerpen/2100/20315980'
response = requests.get(url, headers= headers)
soup = BeautifulSoup(response.content, 'html')

# Parse the content to find the <script> tag containing "window.classified"
script_tag = soup.find('script', string=re.compile(r'window\.classified\s*='))

print(script_tag.text.strip())

if script_tag:
    # Extract the JSON part from the script content
    match = re.search(r'window\.classified\s*=\s*(\{.*?\});', script_tag.string)
    if match:
        classified_data = match.group(1)
        # Parse the JSON data
        classified_dict = json.loads(classified_data)
        with open('thing.txt', 'w') as f:
            f.write(classified_dict)
    else:
        print("JSON data not found within the script tag.")
else:
    print("Script tag with 'window.classified' not found.")