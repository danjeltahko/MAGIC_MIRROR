from API.SL_TRAFFIC.sl import SL
from API.WEATHER.weather import Weather
from API.HUE.hue import Hue
from API.WEATHER.weather_api import Weather_API
from API.AFTONBLADET.aftonbladet import Aftonbladet


class MOA:

    def __init__(self) -> None:

        # API object init
        #self.SL = SL()
        self.weather = Weather()
        self.news = Aftonbladet()
        #self.hue = Hue()

        #self.hue.print_all_lights()

    def get_news(self):
        return self.news.testing()

    """     Weather     """
    def set_location(self, location):
        self.weather.get_geocoding(location)

    def get_forecast(self):
        self.weather.forecast = self.weather.set_forecast()
        return self.weather.forecast
    
    def get_forecast_today(self):
        today_weather = []
        array = self.weather.set_forecast()
        for i in range(7):
            today_weather.append(array[i])
        return today_weather

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

if __name__ == "__main__":
    moa = MOA()
    print(moa.get_news())