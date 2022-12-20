import requests
import json
import os

# takes in valid 3 letter IATA
# returns latitude and longitude in an array
# [latitude, longitude]
# returns a string if the latitude is not found in the API response (most likely b/c of a bad key)
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
#   }
# returns # returns a string if the key "businesses" is not found in the API response
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
        # where do i get a description from?
    return output   


# takes in array of data [latitude, longitude, start, end] yyyy-mm-dd
def booking_api(input):
    latitude = input[0]
    longitude = input[1]
    start = input[2]
    end = input[3]

    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    key = open(path + "/../keys/key_rapid.txt", "r").read()
    key = key.strip()

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
    "units":"metric"}

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()

    hotels = response["result"] # array of hotels
    # print(len(hotels))
    print(json.dumps(hotels[0], indent=2))
    # print(hotels[0]["hotel_name"])
    # print(hotels[0]["address"])

    output = []
    for i in range(5):
        hotel = hotels[i]
        temp = {}
        temp["hotel_name"] = hotel["hotel_name"]
        temp["address"] = hotel["address"]
        temp["min_total_price"] = hotel["min_total_price"]
        temp["latitude"] = hotel["latitude"]
        temp["longitude"] = hotel["longitude"]
        output.append(temp)

    # print(json.dumps(output, indent=2))
    return output



# print("==================== airport_api test ====================")
# print("should be [33.94159, -118.40853]")
# print(airport_api("LAX"))

# print("==================== yelp_api test ====================")
# coords = airport_api("LAX")
# yelp_results = yelp_api(coords)
# print(yelp_results)
# print(json.dumps(yelp_results, indent=2))

# coords.append("2022-12-20")
# coords.append("2033-12-21")
# results = booking_api(coords)
# print(json.dumps(results, indent=2))