#/usr/bin/env python3

# Obtain weather data. Use local if available and not_stale.
# Otherwise, use external data

import argparse
import os.path
import urllib.request
import xml.etree.ElementTree as ET
import datetime, math, os.path

# variables
city_name = ""
province = ""
site_code = ""
language = "e"

# command line arguments (part 1) (part 2 at end of file)
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--current", type=str, dest="current",
    default="temperature, highs_and_lows, condition",
    help="Return one or more current weather statistics")
parser.add_argument("-l", "--location", type=str, dest="location",
    help="The city for which you want to retrieve weather info")
args = parser.parse_args()

if args.location:
    city_name = args.location

# determine if current data is still relevant
def data_is_fresh():

    """
    Returns false if data is older than 10 minutes
    """

    global site_code
    
    # get timestamp for local data
    current_file_timestamp = datetime.datetime.fromtimestamp(
            os.path.getmtime(f'{site_code}.xml'))

    # if local data is older than 10 minutes, it is not fresh
    if str(datetime.datetime.now()) > str(
            datetime.datetime.fromtimestamp(os.path.getmtime(
                f'{site_code}.xml')) + datetime.timedelta(minutes=10)):
        return False    
    else:
        return True



# obtain proper site_code for city_name
# TODO: make this actually do something
def get_site_code(city):
    
    import json

    global city_name
    global province
    global site_code
    global language

    j = json.load(open('city_list.json','r'))

    if city in j:
        city_name = city
        province = j[city]['province']
        site_code = j[city]['site_code']


    site_code = f"{site_code}_{language}"

    return site_code

# get proper url based on city
def get_url_and_parse():

    """
    - Get a fresh copy of the data
    - Save a local copy of the data
    - Parse the XML
    """
    
    global city_name
    global province
    global site_code

    if not site_code:
        site_code = get_site_code(city_name)

    try:
        urllib.request.urlretrieve(
            f"https://dd.weather.gc.ca/citypage_weather/xml/{province}/{site_code}.xml", f"{site_code}.xml")
    except:
        raise Exception("Could not find data for desired location.")
    tree = ET.parse(f"{site_code}.xml")
    return tree.getroot()

# obtain parsed weather data
def get_all_weather_data():

    global city_name
    global site_code

    # if site_code for city is unknown, retrieve it
    if not site_code:
        get_site_code(city_name)

    # if exists local data...
    if os.path.isfile(f"{site_code}.xml"):
    
        # and if local data isn't stale
        if data_is_fresh():

            # then use local data
            tree = ET.parse(f"{site_code}.xml")
            return tree.getroot()
    
        # otherwise, get new data
        else:
            return get_url_and_parse()

    # if no file exists, fetch and use new data
    else:
        return get_url_and_parse()

# return specific weather stats 
def current(query):

    global city_name

    # obtain parsed weather data
    root = get_all_weather_data()

    current_conditions = {
    "condition"         :   root[5][3].text,
    "current_time"      :   root[2][5].text,
    "description"       :   root[6][3][1].text,
    "highs_and_lows"    :   root[6][2][0].text,
    "humidity"          :   root[5][10].text,
    "pressure"          :   root[5][8].text,
    "pressure_trend"    :   root[5][8].attrib['tendency'],
    "sunrise_time"      :   root[9][2][5].text,
    "sunset_time"       :   root[9][4][5].text,
    "temperature"       :   root[5][5].text,
    "time"              :   root[1][6].text,
    "visibility"        :   root[5][9].text,
    "wind_direction"    :   root[5][11][2].text,   
    "wind_gusts"        :   "",
    "wind_speed"        :   root[5][11][0].text,
    }
    
    current_conditions['is_daytime'] = True if \
        current_conditions['current_time'] > current_conditions['sunrise_time'] and \
        current_conditions['current_time'] > current_conditions['sunset_time'] \
        else False

    metric_units = {
    "humidity"          :   "%",
    "pressure"          :   " kPa",
    "temperature"       :   "\u00B0C",
    "visibility"        :   " km",
    "wind_speed"        :   " km/h",
    }

    print("Query:", query)

    if query == "help":
        for k in current_conditions.keys:
            return print(k)
    
    # create empty dict for result
    result = {}
    # create boolean result for description
    description = False


    # TODO: Imperial Units?
    # imperial_units = metric_units
    units = metric_units

    print(f"\nCurrent conditions for {city_name}:\n")

    # remove spaces
    query = query.replace(' ', '')

    # remove spaces and convert csv's to list
    query = query.split(',')

    # iterate over list, print each item and append to "result" dict
    for i in query:
        if i in current_conditions:
            
            # don't print inline description (it comes at the end)
            if i == "description":
                description = current_conditions[i]
            else:
                # Prettify condition format
                pretty_condition = i.replace('_',' ')
                print(f"{pretty_condition.title().ljust(20, '.')} {current_conditions[i]}{units[i] if i in units else ''}")

            result[i] = current_conditions[i]
        else:
            print(f"\"{i.title()}\" not found in current_conditions, ignoring")
    

    # print description if selected
    if description:
        print(f"\n{description}")

    # compliance with licensing terms
    print("\nData Source: Environment and Climate Change Canada")
    print(f"{root[0].text}\n")
    return result



# command line arguments (part 2)
if args.current:
    try:
        current(args.current)
    except:
        print("Malformed query.")
