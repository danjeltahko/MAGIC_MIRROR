from API.SL_TRAFFIC.sl import SL
from API.WEATHER.weather import Weather
from API.HUE.hue import Hue
from API.WEATHER.weather_api import Weather_API


class MOA:

    def __init__(self) -> None:

        # API object init
        self.SL = SL()
        self.weather = Weather()
        #self.hue = Hue()

        #self.hue.print_all_lights()

    """     Weather     """
    def set_location(self, location):
        self.weather.get_geocoding(location)

    def get_forecast(self):
        self.weather.forecast = self.weather.set_forecast()
        return self.weather.forecast

    def get_weather(self):
        self.weather.current_temp = self.weather.set_current_weather()
        return self.weather.current_temp
        

    """     SL      """
    def search_trains(self, travel_org, travel_des):
        self.SL.set_transport(travel_org, travel_des)
        self.SL.create_transport()

    def refresh_trains(self):
        self.SL.create_transport()

    def get_trains(self):
        return self.SL.trains