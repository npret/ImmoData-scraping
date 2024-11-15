# Imports

from ImmoWebScraper.GetListingURLs import quick_get_urls
from ImmoWebScraper.ScrapeListings import quick_parse
from ImmoWebScraper.ParseListingDict import quick_relevant
from ImmoWebScraper.CreateDataFrame import parse_listing_info

# Main script

if __name__ == "__main__":

    # Get listing URLs from search results on ImmoWeb, search page is hard-coded in ImmoWebScraper.GetListingURLs.get_url_list. For a full scrape, page number should = 333, here only a subset of the total number of pages is scraped for example purposes. Returns a list of search result URLs and creates a txt file containing the URLs.

    number_pages = 10
    search_results = quick_get_urls(number_pages)

    # Use previous URL list to solve compound URLs (listings from the search results containing information on a compound sale), and scrape information for every listing from the page html. Returns a list of dictionaries, one per listing containing all information and creates a txt file containing all scraped URLs (including individual ones obtained from compound listings).

    listing_dicts = quick_parse(search_results)

    # Extract relevant information from the obtained dictionaries, returns list of dicts containing only requested info per listing

    relevant_dicts = quick_relevant(listing_dicts)

    # Finally load data in pd.DataFrame, saves df to csv file

    data = parse_listing_info(relevant_dicts)






