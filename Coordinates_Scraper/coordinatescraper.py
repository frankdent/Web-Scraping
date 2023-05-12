import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

latitudes = []
longitudes = []
petrographic_ids_combined = pd.read_csv('petrographic_samples_table.csv')
# for url in petrographic_ids_combined['CoordinatesURLs']:
#     # Make a GET request to the webpage
#     map_response = requests.get(url)

#     # Parse the HTML using Beautiful Soup
#     soup = BeautifulSoup(map_response.text, "html.parser")

#     # Find the <div> element containing the latitude and longitude information
#     map_div = soup.find("div", {"id": "map"})
#     default_markers = map_div.get("data-default-markers")

#     # Extract the latitude and longitude from the "data-default-markers" attribute
#     default_markers = json.loads(default_markers.replace('&quot;', '"'))
#     marker_id = next(iter(default_markers[0]))
#     marker = default_markers[0][marker_id]
#     latitude, longitude = marker['coordinate']
#     latitudes.append(latitude)
#     longitudes.append(longitude)

# petrographic_ids_combined['lat'] = latitudes
# petrographic_ids_combined['long'] = longitudes

# descriptions = []
# inclusions = []
# petrographic_group = []
# for url in petrographic_ids_combined['InclusionsURLs'][0:3]:
#     # Make a GET request to the webpage
#     inclusion_reponse = requests.get(url)

#     # Parse the HTML using Beautiful Soup
#     soup_desc = BeautifulSoup(inclusion_reponse.text, "html.parser")
#     soup_incl = BeautifulSoup(inclusion_reponse.text, "html.parser")

#     # Find the <div> element containing the description information
#     description = soup_desc.find("div", {"class": "col-sm-12"})
#     descriptions.append(description.p.text)

#     # Find the <div. element
#     inclusion = soup_desc.find("div", {"class": "col-sm-6"})
#     inclusions.append(inclusion.find_next('p').find_next('p').text.strip())

# petrographic_ids_combined['Description'] = descriptions
# petrographic_ids_combined['Inclusions'] = inclusions
# petrographic_ids_combined['Description'] = descriptions
# print(descriptions)
# print(inclusions)

# url = 'https://www.levantineceramics.org/petrographics/5034-004'
# inclusion_reponse = requests.get(url)
# soup_incl = BeautifulSoup(inclusion_reponse.text, "html.parser")
# info = soup_incl.find("div", {"id": "petrographic_information"})

# print(info.find_next('p').find_next('p').find_next('p').find_next('p').text.strip())

descriptions = []
inclusions = []
petrographic_group = []
for url in petrographic_ids_combined['InclusionsURLs'][10:11]:
    # Make a GET request to the webpage
    inclusion_reponse = requests.get(url)

    # Parse the HTML using Beautiful Soup
    soup_desc = BeautifulSoup(inclusion_reponse.text, "html.parser")
    soup_incl = BeautifulSoup(inclusion_reponse.text, "html.parser")

    # Find the <div> element containing the description information
    description = soup_desc.find("div", {"class": "col-sm-12"})
    #descriptions.append(description.p.text)
    print(url)
print(descriptions)
