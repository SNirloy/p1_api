import requests
import json
import os

# takes in valid 3 letter IATA
# returns latitude and longitude in an array
# [latitude, longitude]

# returns a string if the key "latitude" is not found in the API response (most likely b/c of a bad key)
# "An error occured. Try checking your API key."
def airport_api(airport_code):
    url = "https://airport-info.p.rapidapi.com/airport"

    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    # print(path)
    key = open(path + "/../keys/key_rapid.txt", "r").read()
    key = key.strip()
    # key = "invalid key test"
    # print(key)

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "airport-info.p.rapidapi.com"
    }

    querystring = {"iata": airport_code}
    # print("querystring: " + str(querystring))

    # response is a dict of what the API returns
    response = requests.get(url, headers=headers, params=querystring).json()
    # print(response)

    if "latitude" not in response.keys():
        output = "An error occured. Try checking your API key."
    else:
        output = [response["latitude"], response["longitude"]]
    return(output)


# takes in array of numbers [latitude, longitude]
# returns array of 5 (can try diff numbers later) businesses and restaurants within a 5 mile radius of the input location
# each element in the array is a dictionary for one business containing the following info
# {
#     "name": "Benny's Tacos & Rotisserie Chicken - Westchester",
#     "display_address": "7101 W Manchester Ave",
#     "url": "https://www.yelp.com/biz/bennys-tacos-and-rotisserie-chicken-westchester-los-angeles?adjust_creative=LUk6VM2I0dwxuj2MZku81w&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=LUk6VM2I0dwxuj2MZku81w",
#     "price": "$$",
#     "rating": 4.5,
#     "distance": 1.4,
#     "latitude": 33.95998,
#     "longitude": -118.41685
#     "tags": [
#         "Mexican",
#         "Tex-Mex"
#     ]
# }

# returns a string if the key "businesses" is not found in the API response
# "An error occured. Try checking your API key."
def yelp_api(location):
    # print(location)
    latitude = location[0]
    longitude = location[1]

    # 5 miles aprox 8000 meters
    url = "https://api.yelp.com/v3/businesses/search" +\
    f"?latitude={latitude}" +\
    f"&longitude={longitude}" +\
    "&radius=8000" +\
    "&sort_by=best_match" +\
    "&limit=5"

    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    # print(path)
    key = open(path + "/../keys/key_yelp.txt", "r").read()
    key = key.strip()
    # key = "invalid key test"
    # print(key)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + key
    }

    response = requests.get(url, headers=headers).json()
    # print(json.dumps(response, indent=2))
    
    # error message/string in case something happens
    if "businesses" not in response.keys():
        return "An error occured. Try checking your API key."

    # array of businesses, each element is a dictionary with one businesses' info
    businesses = response["businesses"] 
    # print(json.dumps(businesses, indent=2))

    num_businesses = len(businesses) # same as limit in url
    # print("number of businesses/restaurants: " + str(num_businesses))
    
    output = []
    for i in range(num_businesses):
        all_info = businesses[i] # dict for one business
        output.append({})
        main_info = output[i] # dict for one business
        main_info["name"] = all_info["name"]
        main_info["display_address"] = all_info["location"]["display_address"][0]
        main_info["url"] = all_info["url"]
        main_info["price"] = all_info["price"]
        main_info["rating"] = all_info["rating"]
        # distance is in miles, rounded to the nearest 10th
        # distance is distance btwn two points, not driving distance
        main_info["distance"] = round(all_info["distance"] * 0.000621371, 1)
        main_info["latitude"] = all_info["coordinates"]["latitude"]
        main_info["longitude"] = all_info["coordinates"]["longitude"]
        # getting tags
        categories = all_info["categories"] # array of dictionaries
        # print(categories)
        num_categories = len(categories)
        # print(num_categories)
        tags = []
        for i in range(num_categories):
            tags.append(categories[i]["title"])
        main_info["tags"] = tags
    return output   


# takes in array of data [latitude, longitude, start date, end date] 
# dates are in yyyy-mm-dd
# currently looks for 1 room for 2 adults, change this in future?
# locale and currency are en-us and USD, have not tested inputting foreign airports coords with these parameters
# returns array of up to 5 (can try diff numbers later) hotels, array has 5 hotels majority of the time, not sure what search radius is
# each element in the array is a dictionary for one business containing the following info
# {
# "hotel_name": "The Metric - Los Angeles Downtown",
# "address": "285 Lucas Avenue",
# "min_total_price": 243,
# "latitude": 34.058728,
# "longitude": -118.261664,
# "distance": 18.8
# }

# returns a string if the key "result" is not found in the API response
# "An error occured. Try checking your API key. Additionally, make sure your dates have not already passed, your dates are within 30 days of each other, and your start date is before your end date."

# returns a string if no hotels are found (will probably never run into this though because airports are bound to have hotels nearby)
# "No results were found. Try a different location."
def booking_api(input):
    latitude = input[0]
    longitude = input[1]
    start = input[2]
    end = input[3]

    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    key = open(path + "/../keys/key_rapid.txt", "r").read()
    key = key.strip()
    # key = "invalid key test"

    url = "https://booking-com.p.rapidapi.com/v1/hotels/search-by-coordinates"

    querystring = {"locale":"en-us",\
    "filter_by_currency":"USD",\
    "order_by":"popularity",\
    "latitude":latitude,\
    "longitude":longitude,\
    "checkin_date":start,\
    "checkout_date":end,\
    "room_number":"1",\
    "adults_number":"2",\
    "units":"imperial"}

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    # print(response)

    # response if invalid API key:
    # {'message': 'You are not subscribed to this API.'}
    if "result" not in response.keys():
        return "An error occured. Try checking your API key. Additionally, make sure your dates have not already passed, your dates are within 30 days of each other, and your start date is before your end date."

    hotels = response["result"] # array of hotels
    num_hotels = len(hotels)
    # print("number of results: " + str(num_hotels))

    if num_hotels == 0:
        return "No results were found. Try a different location."
    
    # print("info for one hotel:")
    # print(json.dumps(hotels[0], indent=2))

    # if statement should work, haven't been able to test for a location with < 5 results though
    if num_hotels < 5:
        num_hotels_returned = num_hotels
    else:
        num_hotels_returned = 5
    
    # print("number of hotels to return: " + str(num_hotels_returned))

    output = []
    for i in range(num_hotels_returned):
        hotel = hotels[i]
        temp = {}
        temp["hotel_name"] = hotel["hotel_name"]
        temp["address"] = hotel["address"]
        temp["min_total_price"] = int(hotel["min_total_price"])
        temp["latitude"] = hotel["latitude"]
        temp["longitude"] = hotel["longitude"]
        temp["distance"] = round(float(hotel["distance"]), 1)
        output.append(temp)
    return output  

def map_api(coordinates):
    return f"""
    <div>
        <iframe width="500" height="400" frameborder="0" src="https://www.bing.com/maps/embed?h=400&w=500&cp={coordinates[0]}~{coordinates[1]}&lvl=13&typ=d&sty=r&src=SHELL&FORM=MBEDV8" scrolling="no">
        </iframe>
        <div style="white-space: nowrap; text-align: center; width: 500px; padding: 6px 0;">
            <a id="largeMapLink" target="_blank" href="https://www.bing.com/maps?cp={coordinates[0]}~{coordinates[1]}&amp;sty=r&amp;lvl=13&amp;FORM=MBEDLD">View Larger Map</a> &nbsp; | &nbsp;
            <a id="dirMapLink" target="_blank" href="https://www.bing.com/maps/directions?cp={coordinates[0]}~{coordinates[1]}&amp;sty=r&amp;lvl=13&amp;rtp=~pos.{coordinates[0]}_{coordinates[1]}____&amp;FORM=MBEDLD">Get Directions</a>
        </div>
    </div>
"""

# print("==================== airport_api test ====================")
# print("should be [33.94159, -118.40853]")
# print(airport_api("LAX"))

# print("==================== yelp_api test ====================")
# # coords = airport_api("LAX")
# coords = [33.94159, -118.40853] # LAX
# # coords = [53.333610, -2.849722] # Liverpool Airport
# yelp_results = yelp_api(coords)
# # print(yelp_results)
# print(json.dumps(yelp_results, indent=2))

# print("==================== booking_api test ====================")
# # coords = airport_api("LAX")
# # data = coords
# data = [33.94159, -118.40853]
# data.append("2022-12-30") # start date
# data.append("2022-12-31") # end date
# results = booking_api(data)
# print(json.dumps(results, indent=2))

# print("South Pole Test:")
# data = [90, 45, "2022-12-30", "2022-12-31"]
# results = booking_api(data)
# print(results)

# print("Small Town Test (Sherrill, NY):")
# print("Trying to make sure booking_api() works when there's < 5 results from the API but even this small town has 15 results")
# data = [43.0737, -75.5982, "2022-12-30", "2022-12-31"]
# results = booking_api(data)
# print(json.dumps(results, indent=2))

# print("Dates Too Far Apart Test")
# data = [90, 45, "2023-01-01", "2023-12-31"]
# results = booking_api(data)
# print(results)

# print("Dates Already Passed Test")
# data = [90, 45, "2021-01-01", "2021-12-31"]
# results = booking_api(data)
# print(results)

# print("Checkout Before Checkin Test")
# data = [90, 45, "2022-12-31", "2022-12-30"]
# results = booking_api(data)
# print(results)