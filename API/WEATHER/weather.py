import requests 
import json
from API.api_keys import WEATHER_KEY

class Weather:

    def __init__(self) -> None:
        self.api_key = WEATHER_KEY
        
        self.lat = 50
        self.lon = 17

    
    def get_geocoding(self, city):
        
        # https://openweathermap.org/api/geocoding-api
        URL = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid{self.api_key}"

        response = requests.get(URL)
        data = json.loads(response.text)

        print(data)


    def get_current_weather(self):

        # https://openweathermap.org/current
        URL = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid{self.api_key}"

        response = requests.get(URL)
        data = json.loads(response.text)

        print(data)


    def get_forecast(self):

        # https://openweathermap.org/forecast5
        URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.lon}&appid={self.api_key}"


    def get_air_pollution(self):

        # https://openweathermap.org/api/air-pollution
        URL = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={self.lat}&lon={self.lon}&appid={self.api_key}"






"""
lat, lon (required) - Geographical coordinates
appid (required) - Your unique API key

exclude (optional) - exclude some parts of the weather data, commadelimited list without spaces
                    // current
                    minutely
                    hourly
                    daily
                    alerts

units (optional) - units of measurement [standard, metric, imperial]
                    standard unit will be applied by default

lang (optional) - output in your language

"""