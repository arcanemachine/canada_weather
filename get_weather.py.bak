#/usr/bin/env python3

# Obtain weather data. Use local if available and not_stale.
# Otherwise, use external data


import os.path
import urllib.request
import xml.etree.ElementTree as ET

import datetime, math, os.path


def data_is_fresh():

    """
    Returns false if data is older than 10 minutes
    """
    
    current_file_timestamp = datetime.datetime.fromtimestamp(
            os.path.getmtime('s0000661_e.xml'))

    if str(datetime.datetime.now()) > str(
            datetime.datetime.fromtimestamp(os.path.getmtime(
                's0000661_e.xml')) + datetime.timedelta(minutes=10)):
    
        return False
    
    
    else:
        return True



# URL parameter strings
# TODO: Update these to accept dynamic values

language = "e"
province = "AB"
site_code = f"s0000661_{language}"
city_name = "Grande Prairie"


def get_url_and_parse():

    """
    - Get a fresh copy of the data
    - Save a local copy of the data
    - Parse the XML
    """

    urllib.request.urlretrieve(
            "https://dd.weather.gc.ca/citypage_weather/xml/AB/s0000661_e.xml", "s0000661_e.xml")
    tree = ET.parse("s0000661_e.xml")
    return tree.getroot()

# if exists local data...
if os.path.isfile('s0000661_e.xml'):
    
    # and if local data isn't stale
    if data_is_fresh():

        # then use local data
        tree = ET.parse('s0000661_e.xml')
        root = tree.getroot()
    
    # otherwise, get new data
    else:
        root = get_url_and_parse()

# if no file exists, fetch and use new data
else:
    
    root = get_url_and_parse()


# Print some stats
print(f"Current temperature in {city_name}, {province}: {root[5][5].text} degrees Celsius")
