from math import floor
import requests
import json
import re

htmlregex = re.compile('<.*?>')

LOCATIONS_ID = {
    "Cafe Ventanas": 0,
    "WongAvery Library": 1,
    "WongAvery Grad Study": 2,
    "Rimac": 3,
    "Main Gym": 4,
    "6th Restaurant": 5,
    "The Bistro": 6,
    "Roger's Market": 7,
    "Canyon Vista" : 8,
    "Geisel Library": 9,
    "64 Degrees": 10,
    "Foodworx": 11,
    "Pines": 12,
    "OceanView Terrace": 13,
    "Price Center": 14,
    "Student Services Center": 15,
    "Parking Offices": 16,
    "7th Market": 17,
    "Club Med": 18}

GEISEL_FLOOR_API_INDEX = { 
    1:[0,1],
    "1E": [0],
    "1W": [1],
    "2E": [2],
    "2W": [3],
    2:[2,3],
    4:[4],
    5:[5],
    6:[6],
    7:[7],
    8:[8],
    "TLC": [9]


}

API_URL = "https://waitz.io/live/ucsd"
API_TREND_URL = "https://waitz.io/compare/ucsd"
PEAK_HOURS_INDEX = 2
NEXT_HOUR_INDEX = 0
CROWDED_DAY_COMPARE_INDEX = 1

#calls for rimac info and returns dict
def get_area_info(area):
    api_results = requests.get(API_URL)
    location_data = json.loads(api_results.text)
    area_id = LOCATIONS_ID[area]

    return location_data["data"][area_id]

def get_trend_info(area):
    api_results = requests.get(API_TREND_URL)
    location_data = json.loads(api_results.text)
    area_id = LOCATIONS_ID[area]

    return location_data["data"][area_id]
    
def parse_summary(summary):
    cap_index = summary.find(')')
    summary = summary[:cap_index] + " capacity" + summary[cap_index:]
    return summary
    
def clean_html(html):
    clean = re.sub(htmlregex, '', html)
    return clean

def rimac_status():

    rimac_info = get_area_info("Rimac") 
    rimac_trend_info = get_trend_info("Rimac")
    

    status_message = "Rimac Weight Room is currently "

    #give busyness if rimac is open 
    is_rimac_open = rimac_info["isOpen"]

    if not is_rimac_open:
        status_message += "closed"
    else:
        summary = rimac_info["locHtml"]["summary"]
        status_message += parse_summary(summary)
        status_message += "\n" + clean_html(rimac_trend_info["comparison"][PEAK_HOURS_INDEX]["string"])
 
    return status_message

def main_gym_status():

    main_gym_info = get_area_info("Main Gym")
    status_message = "The Main Gym is currently "

    #give busyness if main gym is open 
    is_main_gym_open = main_gym_info["isOpen"]

    if not is_main_gym_open:
        status_message += "closed"
    else:
        summary = main_gym_info["locHtml"]["summary"]
        status_message +=  parse_summary(summary)

 
    return status_message



def geisel_floor_status(floor=None):

    geisel_info = get_area_info("Geisel Library")
    status_message = ''
 
    if not geisel_info["isOpen"]:

        return "geisel is not open!"

#if no floor was provided, print least busy floors 
    if floor == None:
        return least_busy_geisel()

    #floor is out of bounds
    elif floor == 3 or floor > 8 or floor < 1:

        return "please enter a valid floor"

    #get a specific floor
    else:
        floor_ids = GEISEL_FLOOR_API_INDEX[floor]

        for floor_id in floor_ids:
            
            floor_info = geisel_info["subLocs"][floor_id]
            floor_summary = floor_info["subLocHtml"]["summary"]

            if floor_summary == "Closed":
                status_message += "This floor is closed!"
            else:
                status_message += floor_info["name"] + ": " + parse_summary(floor_summary) + "\n"

    return status_message.strip()


def least_busy_geisel():
    geisel_info = get_area_info("Geisel Library")
    status_message = 'Here are the least busy floors in geisel right now: \n\n'
    floors = []

    for location in geisel_info["bestLocations"]:
        floor_index = GEISEL_FLOOR_API_INDEX[abbreviation_fix(location["abbreviation"])]
        
        for index in floor_index:
            floor_info = geisel_info["subLocs"][index]
            floor_summary = floor_info["subLocHtml"]["summary"]

            if floor_summary == "Closed":
                continue
            else: 
                print(floor_index[0])
                floors.append(floor_index[0])

            status_message += floor_info["name"] + ": " + parse_summary(floor_summary) + "\n"

    #Geisel is never marked as "closed" and will leave TLC as "open"
    #if its the only one in the list, its closed.
    if len(floors) == 1 and 9 in floors:
        return "Geisel is closed!"

    return status_message.strip()

def abbreviation_fix(arg):
    if isinstance(arg, str) and arg.isdigit():
        return int(arg)
    else:
        return arg
        
