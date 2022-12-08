import requests

# returns latitude and longitude of inputted airport in an array
# airport_code is 3 or 4 letters and valid code
# any bad input is dealt with __init__.py
def airport_api(airport_code):
    url = "https://airport-info.p.rapidapi.com/airport"

    querystring = {}

    if len(airport_code) == 4: # 4 letter ICAO code
        querystring["icao"] = airport_code
        print("ICAO code added to querystring")
    else: # 3 letter IATA code
        querystring["iata"] = airport_code
        print("IATA code added to querystring")

    print("querystring: " + str(querystring))

    headers = {
        "X-RapidAPI-Key": "57757685bemsh76f30b0ffcfea52p1f8aacjsna219a89367bf",
        "X-RapidAPI-Host": "airport-info.p.rapidapi.com"
    }

    # response is a dict of what the API returns
    response = requests.get(url, headers=headers, params=querystring).json()

    print(response)

    output = [response["latitude"], response["longitude"]]
    return(output)


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



print(airport_api("LAX"))
print(airport_api("KLAX"))