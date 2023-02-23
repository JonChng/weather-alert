import requests
import dotenv
import os
from twilio.rest import Client

dotenv.load_dotenv()


api_key = os.environ["WEATHER_API"]
twillio_id = os.environ["TWILLIO_ID"]
twillio_API_key = os.environ["TWILLIO_API"]

params = {
    "lat":1.290270,
    "lon": 103.851959,
    "exclude":"minutely,current,daily",
    "appid": api_key
}

API = f"https://api.openweathermap.org/data/3.0/onecall"

response = requests.get(API, params=params)
response.raise_for_status()
data = response.json()["hourly"]
twelve_hours = data[0:12]

will_rain = False

for i in twelve_hours:
    weather = i["weather"][0]["id"]
    if int(weather) < 700:
        will_rain = True

if will_rain:
    client = Client(twillio_id, twillio_API_key)
    message = client.messages\
        .create(
        body="It's going to rain. Remember to bring an umbrella!",
        from_= os.environ["TWILLIO_NUMBER"],
        to=os.environ["MY_NO"]
    )
    print(message.status)



