'''
Web scraper to scrape the www.ecozones.ca website for ecoregion descriptions
Note: This will output 'No Data' where there are duplicate regions. They
re-use the same url for their duplicate entries so we will have to find
which areas were duplicated and manually add it.
'''

__author__ = "François d'Entremont"

import requests
import pandas as pd
from bs4 import BeautifulSoup

urls = []
ecoregion_id = []
names = []
descriptions = []
# The urls that store the description information are formed using their ids.
# They reuse the same url as the first if there is a duplicate.
# Looping through 217 IDs and storing their URLs
for i in range(217):
    urls.append(f'http://www.ecozones.ca/english/region/{i+1}.html')

# Looping through the URLs to grab the name and description information
for i, url in enumerate(urls):
    # Make a GET request to the webpage
    reponse = requests.get(url)

    # Parse the HTML using Beautiful Soup
    soup = BeautifulSoup(reponse.text, "html.parser")

    # Find the elements containing the name and description information
    name = soup.find("h1").text
    try:
        desc = soup.find('p').text
    except:
        desc = 'No Data'

    # Append the data to their respected list
    names.append(name)   
    descriptions.append(desc)
    ecoregion_id.append(f'{i+1}')

# Create a pandas dataframe with list information
df = pd.DataFrame({'ecoregion_name': names,
                   'ecoregion_description': descriptions,
                   'ecoregion_id': ecoregion_id})

# Export the dataframe to csv
df.to_csv('ecoregion_descriptions.csv', index = False, encoding='utf-8')
