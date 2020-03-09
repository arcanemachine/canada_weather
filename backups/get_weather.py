#/usr/bin/env python3

# Obtain weather data. Use local if available and not_stale.
# Otherwise, use external data

import argparse
import os.path
import urllib.request
import xml.etree.ElementTree as ET
import datetime, math, os.path

# import weather_support


# command line arguments (part 1) (part 2 at end of file)
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--current", type=str, dest="current",
    help="Return one or more current weather statistics")
args = parser.parse_args()


# determine if current data is still relevant
def data_is_fresh():

    """
    Returns false if data is older than 10 minutes
    """
    
    # get timestamp for local data
    current_file_timestamp = datetime.datetime.fromtimestamp(
            os.path.getmtime('s0000661_e.xml'))

    # if local data is older than 10 minutes, it is not fresh
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

# obtain proper site_code for city_name
# TODO: make this actually do something
def get_site_code(city_name):
    return "Grande Prairie"

# get proper url based on city
def get_url_and_parse():

    """
    - Get a fresh copy of the data
    - Save a local copy of the data
    - Parse the XML
    """
    
    # TODO: dynamic site_code
    #global site_code
    #
    #if not site_code:
    #    site_code = get_site_code(city_name)

    urllib.request.urlretrieve(
            "https://dd.weather.gc.ca/citypage_weather/xml/AB/s0000661_e.xml", "s0000661_e.xml")
    tree = ET.parse("s0000661_e.xml")
    return tree.getroot()

# return parsed weather data
def get_all_weather_data():

    # if exists local data...
    if os.path.isfile('s0000661_e.xml'):
    
        # and if local data isn't stale
        if data_is_fresh():

            # then use local data
            tree = ET.parse('s0000661_e.xml')
            return tree.getroot()
    
        # otherwise, get new data
        else:
            return get_url_and_parse()

    # if no file exists, fetch and use new data
    else:
        return get_url_and_parse()

# return specific weather stats 
def current(query):

    root = get_all_weather_data()

    current_conditions = {
    "condition"     :   root[5][3].text,
    "temperature"   :   root[5][5].text,
    }

    # single query
    if ',' not in query:
        # return answer if found
        if query in current_conditions:
            return current_conditions[query]
        else:
            return "nothing found"
    
    # multiple queries
    else:
        result = {}
        query = query.split(',')
        for i in query:
            if query in current_conditions:
                
                # print lines when run from command line
                if args.current:
                    print(f"result[i] = current_conditions[i]")
                
                # append to dict "result" if run as method call
                if not args.current:
                    result[i] = current_conditions[i]
            else:
                print(f"{i} not found in current_conditions, ignoring")


# Print some stats
# print(f"Current temperature in {city_name}, {province}: {root[5][5].text} degrees Celsius")

# command line arguments (part 2)
if args.current:
    
    if ',' not in args.current:
        print(f"{args.current} = {current(args.current)}")
    else:
        for i in args.current:
            print(f"{i} = {current(i)}")

    # TODO: Multiple arguments for get_weather.current
    #if ',' in args:
    #    args.split(',')
    #    for i in args:
    #        return

