# **ImmoData-scraping**

![Belgian houses cartoon.](https://www.shutterstock.com/image-vector/seamless-border-cute-retro-houses-600nw-1111423082.jpg)

[Introduction](#Introduction)     |     [Description](#Description)     |       [Installation](#Installation - Environment setup)    |       [Usage](#Usage)    |[Contributors](#Contributors)    |      [Timeline](#Timeline)       |       [List of Improvements](#list-of-improvements)  

## **Introduction**

The contents of this repo represent the first group project in a series aimed at completing a data science workflow from start (data collection) to finish (modelling using machine learning) during my AI and Data science bootcamp training at BeCode (Brussels, Belgium). The final goal is to create a machine learning model capable of predicting real estate prices in Belgium.

The specific aims for this project are to:
1. Scrape a website for real estate data
2. Build a dataset from scratch
3. Implement a strategy to collect as much data as possible
4. Implement some data cleaning and restitute the data ready for analysis in dataframe and csv form

Specifications for the final dataset are:
- Obtain at least 10.000 entries for real estate properties
- Data should be collected concerning some 19 variables, including locality, property type, price, liveable area, number of rooms, garden present or not etc...
- The observations should come from all over Belgium
- There should be no empty rows in the data
- Record variables as much as possible in numerical values (e.g. 0 or 1 for binary categorical data, multiple categories where appropriate)

My personal contributions to this project can be found in the contributors section of this README.

The repository contains multiple branches
- Main: contains the code for scraping the chosen website
- KevinDataClean: my working branch, containing in addition a jupyter notebook used for data cleaning and start of exploratory data analysis
- Other working branches for contributors

## **Description**
## Scraping real estate data from a website.

This program scrapes houses and apartments data from immoweb.be by: 
- getting the real estate listing URLs from search pages and exporting to a txt file (ImmoWebScraper/GetListingURLs.py)
- handling pages for compound listings (new development, multiple properties on one page) by finding the individual listing URLs
- exporting all finally scraped URLs in a txt file
- getting data for each URL and parsing the raw data to a list of dictionaries (ImmoWebScraper/ScrapeListings.py)
- getting relevant data for each property, storing in a list of dictionaries (ImmoWebScraper/ParseListingDict.py)
- storing the data in a dataframe and writing the data to a CSV file (ImmoWebScraper/CreateDataFrame.py)
- To speed up the process, each step makes use of multiprocessing

Packages used:
- Requests
- Beautifulsoup
- multiprocessing
- json
- re
- pandas

## **Installation - Environment setup**

You can create a virtual environment for the script using venv.
```shell
python -m venv C:\path\to\new\virtual\environment
```

Or using conda.
```shell
conda create --name <my-env>
conda activate <my-env>
```

Included in the repository is a cross-platform environment.yml file, allowing to create a copy of the one used for this project. The environment name is given in the first line of the file.
```shell
conda env create -f environment.yml
conda activate wikipedia_scraper_env
conda env list #verify the environment was installed correctly
```

## **Usage**

Create a local copy of the repository by cloning and navigate to the directory using CLI. Running the following command runs the main.py script, which will scrape the real estate website search pages (for houses and apartments excluding annuity sales) for a specified number of pages. 333 pages were scraped for the project, resulting in over 15.000 listings. However, for the sake of brevity, a much smaller amount of pages is set in the code. This can be changed in the main.py file. The script will create initial URL and full URL lists, as well as export the data in csv format in the Data directory.

```shell
python main.py
```

## **Contributors**
Kevin - https://github.com/kvnpotter
- Day 1: 
  - Worked on solution to acquire data from website using selenium (obsolete, deprecated)
- Day 2:
  - Continued work on getting data using Selenium and scrapy spider (obsolete, deprecated)
  - Found solution using Requests and Beautifulsoup
  - Found dictionary data structure on listing page allowing to obtain data rapidly
  - Started developing functions to get URLs of search results, getting data from individual URLs
- Day 3:
  - Continued development on functions to obtain data from individual URLs
  - Addition of multiprocessing solution to speed up process
  - Finalized data acquisition - up to getting raw data
- Day 4:
  - Wrote docstrings for functions, verified type hints
  - Finalized data acquisition - search result URLs, dealing with compound sale listings, getting raw data from individual URLs, transforming to required data, multiprocessing.
  - Structure of repo and code in modules, integration into main.py
- Challenges:
  - Initial startup of project phase complicated, leading to multiple changes in direction
  - Attribution of tasks not always evident in such a project

Nicole - https://github.com/npret
- Day 1: 
  - Developed solution to get data points from HTML structure using Xpaths (obsolete)
  - Worked on initial solution to deal with pagination (to get urls)
- Day 2:
  - Course change: Moved from Scrapy to BeautifulSoup and Selenium
  - Reworked solution to extract data points using bs4 (obsolete)
- Day 3:
  - Course change: Kevin found a solution to extract all data.
  - Developed get_relevant_info function to extract specific data points from dictionaries.
- Day 4: 
  - Refined get_relevant_info function
  - Researched data cleaning best practices
  - Cleaned dataset(removed duplicates, corrected dtypes, added placeholders for NaN values)
- Challenges:
  - After an initial challenge in dividing responsibilities, our team collaborated effectively, with each member taking ownership of a project section.
  - Initially struggled to decide on a direction, which rendered some of my early work obsolete. However, the previous work informed and improved the next iteration of my section.
  - Github was giving problems.

Patrycja - https://github.com/pschchowah
- Day 1: 
  - read through the project brief 
  - created a trello board (ultimately not used)
  - studied the immoweb listings' html structure
  - explored scrapy Spider (took a DataCamp module)
  - filled in README.md
  - tested ways to get cookies to work with selenium
- Day 2:
  - dealt with Python installations in PyCharm
  - implemented multiprocessing to speed up getting URLs
- Day 3:
  - refined the way URLs were being selected from the search page
  - worked on getting the compound sale listings' individual URLs
- Day 4: 
  - cleaned the dataset by correcting data types and removing duplicates 
  - updated the README.md
- Challenges:
  - work division is not self-evident with this kind of project
  - packages installations proved tricky

## **Timeline**
12 Nov 2024 - project initiated at BeCode Brussels AI & Data Science Bootcamp

15 Nov 2024 - project phase (web scraping and data cleaning) ended


## **List of Improvements**
- Front-end
- Performance
- Code comments
