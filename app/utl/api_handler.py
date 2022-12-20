import requests
import json
import os

# takes in valid 3 letter IATA
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
    "&limit=5" # +\
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
    print(response["businesses"])
    
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
        # main_info["display_phone"] = all_info["display_phone"]
        main_info["url"] = all_info["url"]
        main_info["price"] = all_info["price"]
        main_info["rating"] = all_info["rating"]
        main_info["distance"] = all_info["distance"]
        # desc
        # latitude
        # longitude
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
coords = airport_api("LAX")
# results = yelp_api(coords)
# print(json.dumps(results, indent=2))
coords.append("2022-12-20")
coords.append("2033-12-21")
results = booking_api(coords)
print(json.dumps(results, indent=2))