from API import Aftonbladet, CoinMarketCap, Hue, SL, Trakt, Weather, Fitbit

__version__ = 1.0
__author__ = 'https://github.com/DanjelTahko'

class MOA:

    """ Mamma & Assistent """

    def __init__(self) -> None:

        # SL init
        self.sl = SL()
        self.set_travel("Vällingby", "Sankt Eriksplan")

        self.weather = Weather()
        self.news = Aftonbladet()
        self.hue = Hue()

        self.name = 'Time'
        self.time = ''
        self.connected = 0

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
    def set_travel(self, travel_from:str, travel_to:str):

        # returns a dictionary list with all stations similar to search
        from_stations = self.sl.get_every_station(travel_from)
        to_stations = self.sl.get_every_station(travel_to)
        print(to_stations)
        # sets travel station, index 0 will always be the search /most similar
        self.sl.from_station = from_stations[0]
        self.sl.to_station = to_stations[0]
        print(self.sl.to_station)

    def get_travel(self):
        return self.sl.get_trip()




    # def search_trains(self, travel_org, travel_des):
    #     self.SL.set_transport(travel_org, travel_des)
    #     self.SL.create_transport()

    # def refresh_trains(self):
    #     self.SL.create_transport()

    # def get_trains(self):
    #     array = [self.SL.from_station, self.SL.to_station]
    #     return array

if __name__ == "__main__":
    moa = MOA()
    print(moa.get_news())