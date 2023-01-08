from API import Aftonbladet, CoinMarketCap, Hue, SL, Trakt, Weather, Fitbit, ToDo
from datetime import datetime

__version__ = 1.0
__author__ = 'https://github.com/DanjelTahko'

class MOA:

    """ Mamma & Assistent """

    def __init__(self) -> None:

        # Time & Date init
        self.current_time = "00:00:00"
        self.current_day = "Sön 20 Apr"

        # SL init
        self.sl = SL()
        self.sl_travel = []
        self.last_from_station = "Vällingby"
        self.last_tooo_station = "Sankt Eriksplan"
        self.sl_new = False
        self.__SL__(self.last_from_station, self.last_tooo_station)

        # ToDo init
        self.todo = ToDo()

        self.weather = Weather()
        self.news = Aftonbladet()
        self.hue = Hue()

        self.connected = 0


    """ ### Time & Date ### """
    def __DATETIME__(self):
        self.current_time = self.get_current_time().strftime("%H:%M:%S")
        self.current_day = self.get_current_day()

    def get_current_time(self) -> datetime:
        """ Returns current time datetime.time: 22:50:30"""
        return datetime.strptime(datetime.now().strftime("%m-%d-%y %H:%M:%S"), "%m-%d-%y %H:%M:%S")

    def get_current_day(self) -> str:
        """ Returns current date string: Fre 6 Jan """
        _week = ['Mån','Tis', 'Ons', 'Tor', 'Fre', 'Lör', 'Sön']
        _month = ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec']
        weekday = datetime.today().weekday()
        day = int(datetime.now().strftime('%d'))
        month = int(datetime.now().strftime('%m'))
        return f"{_week[weekday]} {day} {_month[month-1]}"


    """ ### SL Traffic ### """
    def __SL__(self, travel_from:str, travel_tooo:str) -> None:
        self.log_data(f"MOA __init__ : __SL__")
        self.set_new_from_station(travel_from)
        self.set_new_tooo_station(travel_tooo)
        self.set_new_travel()
        
    def set_new_from_station(self, travel_from:str) -> None:
        """ Gets and sets data of travel_from station """
        # sets 'MOA last_from_station' search to travel_from.
        # so we can compare when new search is done
        # and therefor save on our API get request for new ID
        self.last_from_station = travel_from
        # returns a dictionary list with all stations similar to search
        from_stations = self.sl.get_every_station(travel_from)
        # sets travel station, index 0 will always be the search /most similar
        self.sl.from_station = from_stations[0]
        self.log_data(f"MOA SL new 'travel_from' is set: {self.sl.from_station['Name']}")

    def set_new_tooo_station(self, travel_tooo:str) -> None:
        """ Gets and sets data of travel_tooo station """
        # sets 'MOA last_tooo_station' search to travel_to.
        # so we can compare when new search is done
        # and therefor save on our API get request for new ID
        self.last_tooo_station = travel_tooo
        # returns a dictionary list with all stations similar to search
        to_stations = self.sl.get_every_station(travel_tooo)
        # sets travel station, index 0 will always be the search /most similar
        self.sl.to_station = to_stations[0]
        self.log_data(f"MOA SL new 'travel_to' is set: {self.sl.to_station['Name']}")

    def set_new_travel(self) -> None:
        """ Creates travel dictionary list with travel data """
        # sets trip to destination with next 5 departures
        self.sl_travel = self.sl.set_trip()
        if (len(self.sl_travel) > 0):
            self.sl_new = True
            self.log_data("MOA SL: Successfully created new Travel with new train departures")
        else:
            self.log_data("MOA SL: Failed to created new Travel with new trains and departures. (See ERROR for more info)")

    def get_nearest_trip_time(self) -> datetime:
        """ Returns first departure from train/trip in list: 22:50:30 """
        # returns first/nearest departure
        nearest_time = self.sl_travel[0]['origin_time']
        return datetime.strptime(nearest_time, "%m-%d-%y %H:%M:%S")

    def get_travel(self):
        # returns list with trips and their departures
        # return self.sl.get_trip()
        return self.sl_travel

    
    """ ### ToDo ### """
    def get_auth(self):
        return self.todo.authorize()

    def auth_response(self, token):
        self.todo.get_token(token)

    def get_data(self, user_input:str):
        return self.todo.graph_request(user_input)










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

    def convert_datetime_str(self, dt:datetime) -> str:
        dt_str = dt.strftime("%H:%M:%S")
        return dt_str

    def log_data(self, data:str) -> None:
        with open("log/logged.txt", "a") as file:
            dt = datetime.now().strftime("%m/%d/%y %H:%M:%S")
            log_file = f"[{dt}] - {data}\n"
            file.write(log_file)
            file.close()
        

    



if __name__ == "__main__":
    moa = MOA()