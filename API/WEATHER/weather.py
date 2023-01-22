from API.api_keys import WEATHER_KEY
from urllib import parse
import requests
import json
import datetime

class Weather:

    def __init__(self):

        self.location  = None
        self.latitude  = None
        self.longitude = None
        self.country   = None

    def set_location(self, city:str) -> bool:
        """ Set location and get lat & lon from search """
        URL = f"https://api.openweathermap.org/geo/1.0/direct?q={parse.quote(city)}&limit=5&appid={WEATHER_KEY}"
        response = requests.get(URL)
        # check get request for success
        if (response.status_code == 200):
            data = json.loads(response.text)

            # if given search exists / returns a similar city/location
            if (len(data) != 0):
                self.latitude  = data[0]["lat"]
                self.longitude = data[0]["lon"]
                self.location  = data[0]["name"]
                self.country   = data[0]["country"]

            # if given search doesnt exist. Set location to "Uncertain. US"
            else:
                URL = f"https://api.openweathermap.org/geo/1.0/direct?q=Uncertain&limit=5&appid={WEATHER_KEY}"
                response = requests.get(URL)
                data = json.loads(response.text)
                self.latitude  = data[0]["lat"]
                self.longitude = data[0]["lon"]
                self.location  = data[0]["name"]
                self.country   = data[0]["country"]

            return True
            
        else:
            return False

    def set_current(self) -> dict:
        """ Returns dictionary with necessary current weather data """
        URL = f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&units=metric&lang=se&appid={WEATHER_KEY}"
        response = requests.get(URL)
        # check get request for success
        if (response.status_code == 200):
            # https://openweathermap.org/weather-conditions <- weather icons??
            current_weather = self.create_weather_object(json.loads(response.text))
            return current_weather
        else:
            return None
    
    def set_forecast(self) -> list:
        """ Returns list with weather data for 5 days with 3 hour interval """

        URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={self.latitude}&lon={self.longitude}&units=metric&lang=se&appid={WEATHER_KEY}"
        response = requests.get(URL)
        if (response.status_code == 200):
            # https://openweathermap.org/weather-conditions
            data = json.loads(response.text)
            forecast_list = []
            for w in data['list']:
                new_weather = self.create_weather_object(w)
                forecast_list.append(new_weather)
            return forecast_list
        else:
            print(f"Could not receive data from API request set_forecast()")
            return None

    def create_weather_object(self, _weather:dict) -> dict:
        """ Extracts data from API request and creates/returns dictionary with necessary data"""
        
        # Add weather description
        weather_description = []
        for w in _weather['weather']:
            weather_description.append(str(w['description']).capitalize())
        
        # Add data to new dictionary 
        weather_object = {
            "temperature": f"{int(_weather['main']['temp'])}°",
            "description": " & ".join(weather_description),
            "icon": f"http://openweathermap.org/img/w/{_weather['weather'][0]['icon']}.png",
            "feels_like": f"{int(_weather['main']['feels_like'])}°",
            "dt": datetime.datetime.strftime(datetime.datetime.fromtimestamp(_weather['dt']), "%m-%d-%y %H:%M:%S"),
            "clouds": f"{_weather['clouds']['all']}%",
            "wind": f"{int(_weather['wind']['speed'])} m/s"
        }

        # if _weather from current_weather. Add sunrise string time to dictionary
        if ("sunrise" in _weather['sys']):
            weather_object['sunrise'] = datetime.datetime.strftime(datetime.datetime.fromtimestamp(_weather['sys']['sunrise']), "%m-%d-%y %H:%M:%S")
        # if _weather from current_weather. Add sunset string time to dictionary
        if ("sunset" in _weather['sys']):
            weather_object['sunset'] = datetime.datetime.strftime(datetime.datetime.fromtimestamp(_weather['sys']['sunset']), "%m-%d-%y %H:%M:%S")
        # if weather is snowing. Add snow to dictionary
        if ("snow" in _weather):
            if ("1h" in _weather['snow']):
                weather_object['snow'] = f"{_weather['snow']['1h']} mm/h"
            else:
                weather_object['snow'] = f"{_weather['snow']['3h']} mm/h"
        # if weather is raining. Add rain to dictionary
        if ("rain" in _weather):
            if ("1h" in _weather['rain']):
                weather_object['rain'] = f"{_weather['rain']['1h']} mm/h"
            else:
                weather_object['rain'] = f"{_weather['rain']['3h']} mm/h"

        return weather_object

if __name__ == "__main__":
    foo = Weather()
    foo.set_location("Vällingby")
    foo.set_forecast()

