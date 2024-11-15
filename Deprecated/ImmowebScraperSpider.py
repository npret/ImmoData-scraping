# Imports

import json
import scrapy
import pandas as pd
import # SELENIUMFUNCTIONS

# Define scrapy spider class

class ImmowebSpider(scrapy.Spider):
    name = 'immoweb'
    start_urls = ['https://www.immoweb.be']  # PASS LIST 10000 URLS or read in line per line from file?
    collected_data = []

    # Define custom headers to mimic a browser request
    #Scrapy Settings: Customize other settings such as DOWNLOAD_DELAY or ROBOTSTXT_OBEY to control the scraping behavior.
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    ## Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0

    def start_requests(self):
        # If you have specific cookies to send, pass them here
        #cookies = {
            #'cookie_name1': 'cookie_value1',
            #'cookie_name2': 'cookie_value2',
            # Add more cookies as needed
        #}

        # Load cookies from the saved file or directly from a variable
        #with open('cookies.json', 'r') as f:
            #cookies = json.load(f)

        cookies = get_cookies #(URL)


        for url in self.start_urls:
            #
            yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            self.log(f"Request to {response.url} successful!")
            # Extract and process data here
            page_content = response.text
            # Example: save the response body to a file
            with open('output.html', 'w', encoding='utf-8') as f:
                f.write(page_content)
            # ADD CODE HERE TO SAVE REQUIRED INFORMATION AND PARSE TO DF

            # Extract data using Scrapy selectors
            data = {
                'titles': response.css('h2.title::text').getall(), #extract all matches as a list
                'links': response.css('h2.title a::attr(href)').getall(),
                'dates': response.css('span.date::text').getall(),
                }
            
            # Create a DataFrame from the extracted data
            df = pd.DataFrame(data)

            # append df to list

            self.collected_data.append(df)

            # Print the DataFrame (for demonstration)
            self.log(f'Parsed data from {response.url}\nDataFrame:\n{df}')

            # Optionally save the DataFrame to a CSV file
            df.to_csv('scraped_data.csv', index=False)

            # Return the DataFrame if you need to pass it to other parts of your code
            return df

        else:
            # ADD RESPONSE URL
            self.log(f"Request failed with status code: {response.status}")

    def closed(self, reason):
        #combine df into one

        final_df = pd.concat(self.collected_data, ignore_index=True)

        # save df

        final_df.to_csv('scraped_data.csv', index= False)
        self.log('Scraping complete')

