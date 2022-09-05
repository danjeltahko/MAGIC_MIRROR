from API.HUE.hue import Hue
from API.WEATHER.weather import Weather
from moa import MOA





fos = Weather()
fos.get_geocoding("Vällingby")
fos.get_current_weather()

