# **ImmoData-scraping**

![Belgian houses cartoon.](https://www.shutterstock.com/image-vector/seamless-border-cute-retro-houses-600nw-1111423082.jpg)

[Description](#Description)     |       [Installation](#Installation)    |       [Usage](#Usage)    |       [Visuals](#Visuals)     |       [Contributors](#Contributors)    |      [Timeline](#Timeline)       |       [List of Improvements](#list-of-improvements)  

## **Description**
Scraping real estate data from a website.

This programme scrapes houses and apartments data from immoweb.be by: 
- taking the URL listings
- getting relevant info for each URL
- writing the data to a CSV file

## **Installation**
You can 'git clone' the repository and use it locally.

## **Usage**
Packages to be installed are: requests, BeautifulSoup, json, os and pandas (requirements file is not available at this point).

## **Visuals**
The html support for this scraper will be scheduled at a later date. Stay tuned!

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
  - Course change: Keven found a solution to extract all data.
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
