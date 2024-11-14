# Imports
 
import pandas as pd

# Functions

def parse_listing_info(relevant_info_dicts: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(relevant_info_dicts)
    df.to_csv('Immoweb_scraping_result.csv', index= False, header= True)
    return df