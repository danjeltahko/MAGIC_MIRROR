from API import Aftonbladet, CoinMarketCap, Hue, SL, Trakt, Weather, Fitbit
from datetime import datetime

__version__ = 1.0
__author__ = 'https://github.com/DanjelTahko'

class MOA:

    """ Mamma & Assistent """

    def __init__(self) -> None:

        # Time & Date init
        self.current_time = self.get_current_time()
        self.current_day = self.get_current_day()

        # SL init
        self.sl = SL()
        self.sl_travel = []
        self.set_new_travel("Vällingby", "Sankt Eriksplan")
        self.sl_refreshed = False

        self.weather = Weather()
        self.news = Aftonbladet()
        self.hue = Hue()

        self.connected = 0


    """ ### Time & Date ### """
    def get_current_time(self) -> datetime.time:
        """ Returns current time datetime.time: 22:50:30"""
        return datetime.strptime(datetime.now().strftime('%H:%M:%S'), '%H:%M:%S').time()

    def get_current_day(self) -> str:
        """ Returns current date string: Fre 6 Jan """
        _week = ['Mån','Tis', 'Ons', 'Tor', 'Fre', 'Lör', 'Sön']
        _month = ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec']
        weekday = datetime.today().weekday()
        day = int(datetime.now().strftime('%d'))
        month = int(datetime.now().strftime('%m'))
        return f"{_week[weekday]} {day} {_month[month-1]}"


    """ ### SL Traffic ### """
    def set_new_travel(self, travel_from:str, travel_to:str) -> None:
        """ Creates travel from most similar search stations """
        # returns a dictionary list with all stations similar to search
        from_stations = self.sl.get_every_station(travel_from)
        to_stations = self.sl.get_every_station(travel_to)
        # sets travel station, index 0 will always be the search /most similar
        self.sl.from_station = from_stations[0]
        self.sl.to_station = to_stations[0]
        # sets trip to destination with next 5 departures
        self.sl_travel = self.sl.set_trip()
        # sets refreshed flag to True, so socket can send new data
        self.sl_refreshed = True

    def refresh_travel(self) -> None:
        """ Refresh creating new travel with earlier search stations """
        self.sl_travel = self.sl.set_trip()

    def get_nearest_trip_time(self) -> datetime.time:
        """ Returns first departure from train/trip in list: 22:50:30 """
        # returns first/nearest departure
        travel_array = self.sl.get_trip()
        nearest_time = travel_array[0]['origin_time']
        return datetime.strptime(nearest_time, '%H:%M:%S').time()

    def get_travel(self):
        # returns list with trips and their departures
        return self.sl.get_trip()



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
        

    



if __name__ == "__main__":
    moa = MOA()
    print(moa.get_news())