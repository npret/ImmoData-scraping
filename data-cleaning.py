import pandas as pd

def clean_data():

    df = pd.read_csv('Immoweb_scraping_result.csv')
    df = df.drop_duplicates(subset='id', keep='first') # remove duplicate entries based on unique id

    # TYPE CONVERSION
    #Convert to string
    df['Locality'] = df['Locality'].astype('string')

    # Conver to int and replace empty values with -1 for True/False columns (1/0)
    df['Fully equipped kitchen'] = df['Fully equipped kitchen'].fillna(-1).astype(int)
    df['Furnished'] = df['Furnished'].fillna(-1).astype(int)
    df['Terrace'] = df['Terrace'].fillna(-1).astype(int)
    df['Garden'] = df['Garden'].fillna(-1).astype(int)
    df['Swimming pool'] = df['Swimming pool'].fillna(-1).astype(int)
    # -1 for NaN
    df['Number of facades'] = df['Number of facades'].fillna(-1).astype(int)


    # Convert to float
    df['Price'] = df['Price'].astype('float')

    #Convert to category
    df['Type of property'] = df['Type of property'].astype('category')
    df['Subtype of property'] = df['Subtype of property'].astype('category')
    df['Type of sale'] = df['Type of sale'].astype('category')
    df['State of the building'] = df['State of the building'].astype('category')


    # Adding placeholders for NaN
    df['Living Area'] = df['Living Area'].fillna(-1)
    df['Terrace area'] = df['Terrace area'].fillna(0) # There is no terrace
    df['Garden area'] = df['Garden area'].fillna(0) #There is no garden
    df['Surface of the land'] = df['Surface of the land'].fillna(-1)
    df['Surface area of the plot of land'] = df['Surface area of the plot of land'].fillna(-1)
    df['State of the building'] = df['State of the building'].cat.add_categories(['UNDEFINED'])
    df['State of the building'] = df['State of the building'].fillna('UNDEFINED')

    # Drop useless col
    # Type of sale - all same data (residential_sale)
    df.drop('Type of sale', axis=1, inplace=True)

    # Save cleaned data to new csv
    df.to_csv('cleaned_immo-data.csv')

