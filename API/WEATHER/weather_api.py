from API.api_keys import WEATHER_KEY
from API.WEATHER.weather_obj import Weather_OBJ
import requests 
import json
import datetime
import math

class Weather_API:

    def __init__(self) -> None:
        self.api_key = WEATHER_KEY
        self.city = None
        self.lat = None
        self.lon = None
        self.units = "metric"

        self.current_temp = None 
        self.forecast = []

        self.get_geocoding("Vällingby")

    
    def get_geocoding(self, city):
        
        # https://openweathermap.org/api/geocoding-api
        self.city = city
        URL = f"https://api.openweathermap.org/geo/1.0/direct?q={self.city}&limit=5&appid={self.api_key}"
        
        response = requests.get(URL)
        data = json.loads(response.text)

        self.lat = data[0]['lat']
        self.lon = data[0]['lon']


    def set_current_weather(self):

        # https://openweathermap.org/current
        URL = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&units={self.units}&appid={self.api_key}"

        response = requests.get(URL)
        data = json.loads(response.text)

        weather_object = self.create_object(data)
        weather_object.timezone = data['timezone']
        weather_object.dt = datetime.datetime.fromtimestamp(float(weather_object.dt-weather_object.timezone))

        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        weather_object.sunrise = datetime.datetime.fromtimestamp(float(sunrise-weather_object.timezone))
        weather_object.sunset = datetime.datetime.fromtimestamp(float(sunset-weather_object.timezone))

        return weather_object

      
    def set_forecast(self):

        # https://openweathermap.org/forecast5
        URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.lon}&units={self.units}&appid={self.api_key}"
        response = requests.get(URL)
        data = json.loads(response.text)
        
        forecast = []

        for weather in data['list']:
            weather_object = self.create_object(weather)
            weather_object.timezone = data['city']['timezone']
            weather_object.dt = datetime.datetime.fromtimestamp(float(weather_object.dt-weather_object.timezone))
            weather_object.sunrise = data['city']['sunrise']
            weather_object.sunset = data['city']['sunset']
            forecast.append(weather_object)
            

        return forecast
            

    def set_air_pollution(self):

        # https://openweathermap.org/api/air-pollution
        URL = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={self.lat}&lon={self.lon}&appid={self.api_key}"

    
    def create_object(self, data):

        new_object = Weather_OBJ()

        new_object.name = self.city
        # ['weather']
        icon = data['weather'][0]['icon']
        new_object.iconurl = f"http://openweathermap.org/img/w/{icon}.png"
        new_object.main = data['weather'][0]['main'].capitalize()
        new_object.description = data['weather'][0]['description'].capitalize()
        # ['main']
        new_object.temp = math.ceil(data['main']['temp'])
        new_object.feels_like = data['main']['feels_like']
        new_object.temp_min = math.ceil(data['main']['temp_min'])
        new_object.temp_max = math.ceil(data['main']['temp_max'])
        new_object.pressure = data['main']['pressure']
        new_object.humidity = data['main']['humidity']
        # ['wind']
        new_object.wind_speed = data['wind']['speed']
        new_object.wind_deg = data['wind']['deg']
        # ['clouds']
        new_object.clouds = data['clouds']['all']
        # TIME
        new_object.dt = data['dt']
        """
        try:
            new_object.rain = data['rain']['1h']
        except:
            print("No rain")
        """
        return new_object