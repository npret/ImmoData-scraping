# Imports
 
import pandas as pd
import json

# Functions

def parse_listing_info(relevant_info_dicts: list[dict]) -> pd.DataFrame:
    """
    Simple function receiving list of listing dictionaries to convert to pd.DataFrame, and export resulting DataFrame to CSV file.

    : param relevant_info_dicts: list: List of dicts to parse.

    : return: pd.DataFrame: DataFrame containing data.
    """
    df = pd.DataFrame(relevant_info_dicts)
    df.to_csv('./Data/Immoweb_scraping_result.csv', index= False, header= True)
    return df

if __name__ == "__main__":

    with open("./Data/relevant_dicts.json", "r") as file:
        relevant_dicts = json.load(file)

    df = parse_listing_info(relevant_dicts)

    print(type(df))
    print(df.shape)
    print(df.head(5))
    print(df.info)