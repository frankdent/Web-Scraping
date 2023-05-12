'''
A webscraper that will scrape the data from the
https://www.levantineceramics.org/petrographics table. 
The Petrographic IDs Combined with the Petrographic Sample no. combine to form
the URLs where we can loop through and grab valuable information such as 
incisions, coordinates, and petrographic group. Result exported to csv
'''
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup

__author__ = "François d'Entremont"

api_url = "https://www.levantineceramics.org/petrographics.json"
# The params variable contains the parameters to be sent with the API request
params = {
    "sEcho": "2",
    "iColumns": "12",
    "sColumns": ",,,,,,,,,,,",
    "iDisplayStart": "0",
    "iDisplayLength": "100"
}
# The columns variable contains a list of column names for the table to be 
# scraped
columns = [
    "Petrographic Sample no.",
    "Vessel registration no.",
    "Site name",
    "Country/region",
    "Period",
    "Thin-section photos",
    "Break photos",
    "Description",
    "Petro-Fabric",
    "Suggested Clay Provenance",
    "Contributors",
    "Action"
]
# create <table> and parse it through pandas
# 61 sets of 100

def extract_string_quote(s):
    """
    Extracts the string between the start of the input string and the first
    double-quote character (").

    Args:
        s (str): The input string to extract from.
        
    Returns:
        str: The substring of s that starts at index 0 and ends at the index
        of the first double-quote character.
    """
    return s[:s.find('"')]



def extract_string_minus(s):
    """
    Extracts the string between the start of the input string and the first
    minus sign (-).

    Args:
        s (str): The input string to extract from.
        
    Returns:
        str: The substring of s that starts at index 0 and ends at the index
        of the first minus sign.
    """
    return s[:s.find('-')]


frames = []
frames_petro_id_combined = []
for i in range(61): #61 times 100
    params['iDisplayStart'] = str(i*100)
    datatable = requests.get(api_url, params).json()
    # An empty list called table is created to store the rows of the table as
    # HTML code
    table = [
    "<tr>" +
    "\n".join(f"<th>{column}</th>" for column in columns) +
    "</tr>"
    ]
    for row in datatable["aaData"]:
        table.append(
        "<tr>" +
        "\n".join(f"<td>{cell}</td>" for cell in row) +
        "</tr>"
        )
    # Each row in the datatable "aaData" has strings of HTML code generated
    # and appended to the table list.
    df = pd.read_html("<table>" + "\n".join(table) + "</table>")[0]
    # This function returns a list of DataFrame objects, one for each table 
    # found in the HTML content
    frames.append(df)
    # The DataFrame is added to a list called frames.
    # The table is then cleared
    table = None
    # Extracting Petrographic IDs + Petrographic Sample no.
    dataframe = pd.DataFrame.from_records(datatable)
    dataframe['Petrographic ID Combined'] = dataframe[
        "aaData"].str.get(0).str[40:].apply(lambda s: extract_string_quote(s))
    frames_petro_id_combined.append(dataframe)
# The result DataFrame is created by concatenating all of the DataFrames in 
# the frames list.
result_table = pd.concat(frames)
# Combining the dataframes from each page
petrographic_ids_combined = pd.concat(frames_petro_id_combined).drop(
    columns=['aaData', 'iTotalDisplayRecords', 'iTotalRecords', 'sEcho']
)

# Extracting the Petrographic IDS from the Combined Petrographic ID + 
# Petrographic Sample # and using it to create URLs for Coordinates
# and Inclusions
petrographic_ids_combined['Petrographic ID'] = (
    petrographic_ids_combined['Petrographic ID Combined']
    .apply(lambda s: extract_string_minus(s))
)
petrographic_ids_combined['CoordinatesURLs'] = (
    'https://www.levantineceramics.org/map?petrographic_id='
    + petrographic_ids_combined['Petrographic ID Combined']
)
petrographic_ids_combined['InclusionsURLs'] = (
    'https://www.levantineceramics.org/petrographics/'
    + petrographic_ids_combined['Petrographic ID Combined']
)
# Let's loop through the Coordinate URLs to extract the coordinates and add it
# to the table.

latitudes = []
longitudes = []

for url in petrographic_ids_combined['CoordinatesURLs']:
    # Make a GET request to the webpage
    map_response = requests.get(url)

    # Parse the HTML using Beautiful Soup
    soup = BeautifulSoup(map_response.text, "html.parser")
    try:
        # Find the <div> element containing the latitude and longitude 
        # information
        map_div = soup.find("div", {"id": "map"})
        default_markers = map_div.get("data-default-markers")

        # Extract the latitude and longitude from the "data-default-markers"
        # attribute
        default_markers = json.loads(default_markers.replace('&quot;', '"'))
        marker_id = next(iter(default_markers[0]))
        marker = default_markers[0][marker_id]
        latitude, longitude = marker['coordinate']
        latitudes.append(latitude)
        longitudes.append(longitude)
    except:
        latitudes.append('Broken link')
        longitudes.append('Broken link')

petrographic_ids_combined['lat'] = latitudes
petrographic_ids_combined['long'] = longitudes

# Now let's scrape the inclusions and descriptions using the same method.
descriptions = []
inclusions = []
petrographic_group = []
for url in petrographic_ids_combined['InclusionsURLs']:
    # Make a GET request to the webpage
    inclusion_reponse = requests.get(url)

    # Parse the HTML using Beautiful Soup
    soup_desc = BeautifulSoup(inclusion_reponse.text, "html.parser")
    soup_incl = BeautifulSoup(inclusion_reponse.text, "html.parser")

    # Find the <div> element containing the description information
    description = soup_desc.find("div", {"class": "col-sm-12"})
    try:
        descriptions.append(description.p.text.strip())
    except:
        descriptions.append('Broken link')
    # Find the <div> element containing the inclusion information
    try:
        info = soup_incl.find("div", {"id": "petrographic_information"})
        inclusion = info.find("div", {"class": "col-sm-6"})
        inclusions.append(
            inclusion.find_next('p')
                     .find_next('p')
                     .text.strip()
        )
    except:
        inclusions.append('Broken link')
    # Find the Local Petrographic Group. We can use the info variable
    # because it's in the same area
    try:
        petrographic_group.append(
            info.find_next('p')
                .find_next('p')
                .find_next('p')
                .find_next('p')
                .text.strip()
        )
    except:
         petrographic_group.append('Broken link')
petrographic_ids_combined['Description'] = descriptions
petrographic_ids_combined['Inclusions'] = inclusions
petrographic_ids_combined['Petrographic_Group'] = petrographic_group

combined_table = pd.concat([result_table, petrographic_ids_combined], axis=1)
# The result is exported to csv
combined_table.to_csv('petrographic_samples_table_final.csv', index = False)
# If you are getting an error, you might have to split it into two batches.
# range(30) for first batch and range(30,61) for second batch and then merge.







