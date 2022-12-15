import requests
import json
import os

# takes in a 3 or 4 letter string
# returns boolean representing if the airport code is valid
# __input__.py ensures airport_code is 3 or 4 letters
# def valid_airport_code(airport_code):
#     url = "https://airport-info.p.rapidapi.com/airport"

#     path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
#     print(path)
#     key = open(path + "/../keys/key_rapid.txt", "r").read()
#     key = key.strip()
#     print(key)
    
#     querystring = {}
#     headers = {
#         "X-RapidAPI-Key": key,
#         "X-RapidAPI-Host": "airport-info.p.rapidapi.com"
#     }

#     if len(airport_code) == 4: # 4 letter ICAO code
#         querystring["icao"] = airport_code
#         # print("ICAO code added to querystring")
#     else: # 3 letter IATA code
#         querystring["iata"] = airport_code
#         # print("IATA code added to querystring")

#     # print("querystring: " + str(querystring))

#     # response is a dict of what the API returns
#     response = requests.get(url, headers=headers, params=querystring).json()
#     # print(response)

#     # True if error is not a key in response
#     # False if error is a key in response
#     return "error" not in response.keys()


# takes in valid 4 letter ICAO or 3 letter IATA
# returns latitude and longitude in an array
def airport_api(airport_code):
    url = "https://airport-info.p.rapidapi.com/airport"

    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    # print(path)
    key = open(path + "/../keys/key_rapid.txt", "r").read()
    key = key.strip()
    # print(key)

    querystring = {}
    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "airport-info.p.rapidapi.com"
    }

    # if len(airport_code) == 4: # 4 letter ICAO code
    #     querystring["icao"] = airport_code
    #     # print("ICAO code added to querystring")
    # else: # 3 letter IATA code
    #     querystring["iata"] = airport_code
    #     # print("IATA code added to querystring")

    querystring["iata"] = airport_code

    # print("querystring: " + str(querystring))

    # response is a dict of what the API returns
    response = requests.get(url, headers=headers, params=querystring).json()
    # print(response)

    output = [response["latitude"], response["longitude"]]
    return(output)

# takes in array of numbers [latitude, longitude]
# returns array of businesses and restaurants within a 5 mile radius of the location
# each element in the array is a dictionary for one business containing the following info
# - name (string)
# - display_address (array where each element is an address line, each element is a string)
# - display_phone (string)
# - url (string)
# - price (string)
# - Hours NEED TO DO THIS
# - rating (float)
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
    "&limit=1" # +\
    # "&term=restaurant"

    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    # print(path)
    key = open(path + "/../keys/key_yelp.txt", "r").read()
    key = key.strip()
    # print(key)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + key
    }

    response = requests.get(url, headers=headers).json()
    # print(json.dumps(response, indent=2))
    # print(response["businesses"])
    
    output = []

    businesses = response["businesses"] # array of businesses, each element is a dictionary with one businesses' info
    num_businesses = len(businesses) # same as limit in url
    print("number of businesses/restaurants: " + str(num_businesses))
    
    for i in range(num_businesses):
        all_info = businesses[i] # dict for one business
        output.append({})
        main_info = output[i] # dict for one business
        main_info["name"] = all_info["name"]
        main_info["display_address"] = all_info["location"]["display_address"]
        main_info["display_phone"] = all_info["display_phone"]
        main_info["url"] = all_info["url"]
        main_info["price"] = all_info["price"]
        main_info["rating"] = all_info["rating"]
    return output   

# takes in array of numbers [latitude, longitude]
# def booking_api(location)


# print("==================== valid_airport_code test ====================")
# print("should be False, False, True, True")
# print(valid_airport_code("AAAA")) # False ICAO
# print(valid_airport_code("LKS")) # False IATA
# print(valid_airport_code("KJFK")) # True ICAO
# print(valid_airport_code("JFK")) # True IATA


print("==================== airport_api test ====================")
print("should be [33.94159, -118.40853]")
# print(airport_api("KLAX"))
print(airport_api("LAX"))
print("==================== yelp_api test ====================")
coords = airport_api("LAX")
results = yelp_api(coords)
print(json.dumps(results, indent=2))
