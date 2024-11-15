# Imports

from multiprocessing import get_context, cpu_count, Pool
import json
from ImmoWebScraper.GetListingURLs import quick_get_urls
from ImmoWebScraper.ScrapeListings import quick_parse, is_compound_sale

def quick_relevant(list_dicts_listings: list[dict],
                   num_processes: int = None) -> list[dict]:
    
    """
    Function allowing to perform parsing with get_relevant_info using multiprocessing.

    : param list_dicts_listings: list: List of dictionaries containing ImmoWeb listing information for each property.
    : param num_processes: int: Number of processes to use in multiprocessing.

    : return: list: List of dicts with required information.
    """

    if num_processes is None:
        num_processes = cpu_count()  # Use the number of available CPUs by default

    dict_index_ranges = [range(i, len(list_dicts_listings), num_processes) for i in range(num_processes)]

    relevant_dicts = []

    with get_context('spawn').Pool(processes=num_processes) as pool:
        results = pool.starmap(get_relevant_info, [(list_dicts_listings, dict_index_range) for dict_index_range in dict_index_ranges])

        for result in results:
            relevant_dicts.extend(result)
            
    return relevant_dicts

def get_relevant_info(list_dicts_listings: list[dict],
                      dict_index_range) -> list[dict]:
    
    """
    Function to extract required information from listing dictionaries.

    : param list_dicts_listings: list: List of dictionaries containing ImmoWeb listing information for each property.
    : param dict_index_range: range: Range of dictionaries to handle from the list, for multiprocessing.

    : return: List of dicts containing required information.
    """
    
    # List will contain dictionaries for each listing containing relevant info
    relevant_info_list = []
    
    # Iterate over each listing in the main dictionary.
    for i in dict_index_range:

        print(f"Parsing listing dict {i}")
        
        listing = list_dicts_listings[i]

        id = None 
        id = listing.get('id')

        locality = None
        locality = listing.get('property', {}).get('location', {}).get('postalCode')

        property_type = None
        property_type = listing.get('property', {}).get('type')

        property_subtype = None
        property_subtype = listing.get('property', {}).get('subtype')

        price = None
        price = listing.get('transaction', {}).get('sale', {}).get('price')

        sale_type = None
        sale_type = listing.get('price', {}).get('type')

        rooms = None
        rooms = listing.get('property', {}).get('bedroomCount')

        living_area = None
        living_area = listing.get('property', {}).get('netHabitableSurface')

        # Need to make sure what the different status posibilies are
        is_kitchen_equipped = None
        if listing.get('property', {}).get('kitchen', {}) != None:
            kitchen_equipped_status = listing.get('property', {}).get('kitchen', {}).get('type')
            if kitchen_equipped_status is not None and kitchen_equipped_status != "None" and kitchen_equipped_status != "":
                kitchen_equipped_status = kitchen_equipped_status.lower()
                if kitchen_equipped_status in ["uninstalled", "usa uninstalled"]:
                    is_kitchen_equipped = 0
                else:
                    is_kitchen_equipped = 1
        else:
            is_kitchen_equipped = None

        # Need to double check status possibilities
        is_furnished = None
        furnished_status = listing.get('transaction', {}).get('sale', {}).get('isFurnished')
        if furnished_status:
            is_furnished = 1
        elif furnished_status == None:
            is_furnished = None
        else:
            is_furnished = 0

        is_fireplace = None
        fireplace_status = listing.get('property', {}).get('fireplaceExists')
        if fireplace_status is not None and fireplace_status != "None" and fireplace_status != "":
            if fireplace_status == True:
                is_fireplace = 1
            else:
                is_fireplace = 0

        is_terrace = None
        terrace_status = listing.get('property', {}).get('hasTerrace')
        if terrace_status is not None and terrace_status != "None" and terrace_status != "":
            if terrace_status == True:
                is_terrace = 1
            else: 
                is_terrace = 0

        terrace_area = None
        terrace_area = listing.get('property', {}).get('terraceSurface')

        is_garden = None
        garden_status = listing.get('property', {}).get('hasGarden')
        if garden_status is not None and garden_status != "None" and garden_status != "":
            if garden_status == True:
                is_garden = 1
            else:
                is_garden = 0

        garden_area = None
        garden_area = listing.get('property', {}).get('gardenSurface')

        # Garden area twice??
        surface_land = None
        surface_land = listing.get('property', {}).get('gardenSurface')

        #surface_land + living area
        surface_area_plot = None
        if listing.get('property', {}).get('land', {}) != None:
            surface_area_plot = listing.get('property', {}).get('land', {}).get('surface')
        else:
           surface_area_plot = None 

        facades = None
        if listing.get('property', {}).get('building', {}) != None:
            facades = listing.get('property', {}).get('building', {}).get('facadeCount')
        else:
            facades = None

        is_pool = None
        pool_status = listing.get('property', {}).get('hasSwimmingPool')
        if pool_status is not None and pool_status != "None" and pool_status != "":
            if pool_status == True:
                is_pool = 1
            else:
                is_pool = 0

        building_state = None
        if listing.get('property', {}).get('building', {}) != None:
            building_state = listing.get('property', {}).get('building', {}).get('condition')
        else:
           building_state = None

        is_compound = None
        if not is_compound_sale(listing):
            is_compound = 'single'
        else:
            is_compound = 'compound'


        #Extract info from listings into a dictionary
        relevant_info = {'id': id,
                         'Locality': locality,
                         'Type of property': property_type,
                         'Subtype of property': property_subtype,
                         'Price': price,
                         'Type of sale': sale_type,
                         'Number of rooms': rooms,
                         'Living Area': living_area,
                         'Fully equipped kitchen': is_kitchen_equipped,
                         'Furnished': is_furnished,
                         'Fireplace': is_fireplace,
                         'Terrace': is_terrace,
                         'Terrace area': terrace_area,
                         'Garden': is_garden,
                         'Garden area': garden_area,
                         'Surface of the land': surface_land,
                         'Surface area of the plot of land': surface_area_plot,
                         'Number of facades': facades,
                         'Swimming pool': is_pool,
                         'State of the building': building_state,
                         'Compound Listing': is_compound
                        }

        # Add dictionary for listing to our list.
        relevant_info_list.append(relevant_info)

    return relevant_info_list

if __name__ == "__main__":

    with open("list_of_dicts.json", "r") as file:
        listing_dicts = json.load(file)

    relevant_info = quick_relevant(listing_dicts)

    print(f"Number of relevant info dicts created {len(relevant_info)}")
    print(relevant_info[-1])

    with open("./ImmoWebScraper/Data/relevant_dicts.json", "w+") as file:
        json.dump(relevant_info, file)
