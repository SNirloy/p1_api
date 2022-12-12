import requests
import json

# takes in a 3 or 4 letter string
# returns boolean representing if the airport code is valid
# __input__.py ensures airport_code is 3 or 4 letters
def valid_airport_code(airport_code):
    url = "https://airport-info.p.rapidapi.com/airport"

    querystring = {}
    headers = {
        "X-RapidAPI-Key": "57757685bemsh76f30b0ffcfea52p1f8aacjsna219a89367bf",
        "X-RapidAPI-Host": "airport-info.p.rapidapi.com"
    }

    if len(airport_code) == 4: # 4 letter ICAO code
        querystring["icao"] = airport_code
        # print("ICAO code added to querystring")
    else: # 3 letter IATA code
        querystring["iata"] = airport_code
        # print("IATA code added to querystring")

    # print("querystring: " + str(querystring))

    # response is a dict of what the API returns
    response = requests.get(url, headers=headers, params=querystring).json()
    # print(response)

    # True if error is not a key in response
    # False if error is a key in response
    return "error" not in response.keys()


# takes in valid 4 letter ICAO or 3 letter IATA
# returns latitude and longitude in an array
def airport_api(airport_code):
    url = "https://airport-info.p.rapidapi.com/airport"

    querystring = {}
    headers = {
        "X-RapidAPI-Key": "57757685bemsh76f30b0ffcfea52p1f8aacjsna219a89367bf",
        "X-RapidAPI-Host": "airport-info.p.rapidapi.com"
    }

    if len(airport_code) == 4: # 4 letter ICAO code
        querystring["icao"] = airport_code
        # print("ICAO code added to querystring")
    else: # 3 letter IATA code
        querystring["iata"] = airport_code
        # print("IATA code added to querystring")

    # print("querystring: " + str(querystring))

    # response is a dict of what the API returns
    response = requests.get(url, headers=headers, params=querystring).json()
    # print(response)

    output = [response["latitude"], response["longitude"]]
    return(output)

# takes in array of numbers [latitude, longitude]
# returns businesses and restaurants within a 5 mile radius of the location
def yelp_api(location):
    # print(location)
    latitude = location[0]
    longitude = location[1]

    # 5 miles aprox 8000 meters
    url = "https://api.yelp.com/v3/businesses/search" +\
    f"?latitude={latitude}" +\
    f"&longitude={longitude}" +\
    "&radius=8000" +\
    "&term=restaurant" +\
    "&sort_by=best_match" +\
    "&limit=2"

    key = open("../keys/key_yelp.txt", "r").read()
    key = key.strip()
    print(key)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + key
    }

    response = requests.get(url, headers=headers).json()

    print(json.dumps(response, indent=2))

    # businesses = requests[B]



# key = open("key_nasa.txt", "r").read() #key is string
# key = key.strip() #removing white space

# @app.route("/")
# def index():
#     api_url = f"https://api.nasa.gov/planetary/apod?api_key={key}" # url with api key
#     web = requests.get(api_url).json() #json data of api_url, web is a dictionary
#     img_url = web["url"] #gets url of img from web dictionary
#     img_title = web["title"]
#     img_explanation = web["explanation"]
#     return render_template("main.html", title=img_title, explanation=img_explanation, url=img_url)

# print("==================== valid_airport_code test ====================")
# print("should be False, False, True, True")
# print(valid_airport_code("AAAA")) # False ICAO
# print(valid_airport_code("LKS")) # False IATA
# print(valid_airport_code("KJFK")) # True ICAO
# print(valid_airport_code("JFK")) # True IATA
# print("==================== airport_api test ====================")
# print("both should be [33.94159, -118.40853]")
# print(airport_api("KLAX"))
# print(airport_api("LAX"))
coords = airport_api("LAX")
yelp_api(coords)
