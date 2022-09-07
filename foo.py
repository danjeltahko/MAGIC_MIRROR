from API.HUE.hue import Hue
from API.WEATHER.weather_api import Weather_API
from API.WEATHER.weather import Weather
from moa import MOA



fos = Weather()

fos.set_forecast()




"""
fos = Weather_API()
fos.get_geocoding("Vällingby")
fos.get_current_weather()
"""
#fos.get_forecast()


