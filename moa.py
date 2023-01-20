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
        self.last_tooo_station = "Sundbyberg"
        self.sl_new = False
        self.__SL__(self.last_from_station, self.last_tooo_station)

        # Weather init
        self.weather = Weather()
        self.weather_location = "Vällingby"
        self.weather_current = {}
        self.weather_forecast = []
        self.weather_refresh = False
        self.weather_time = "00:00:00"
        self.__WEATHER__(self.weather_location)


        # ToDo init
        self.todo = ToDo()
        self.todo_list = {"name": "No Data Available"}
        self.todo_active = False
        self.todo_refreshed = False
        self.todo_prev_time = "00:00"
        self.todo_expires = None

        # Fitbit init
        self.fitbit = Fitbit()
        self.fitbit_list = {"summary": {"hours": 0,"minutes": 0}}
        self.fitbit_active = False
        self.fitbit_refreshed = False



        # self.news = Aftonbladet()
        # self.hue = Hue()

        # General init
        self.connected = 0


    """ ### Time & Date ### """
    def __DATETIME__(self) -> None:
        self.current_time = self.get_current_time().strftime("%H:%M:%S")
        self.current_day = self.get_current_day()

    def get_current_time(self) -> datetime:
        """ Returns current time datetime.time: 23-01-2022 22:50:30"""
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
        """ Returns first departure from train/trip in list: 01-23-2022 22:50:30 """
        # returns first/nearest departure
        nearest_time = self.sl_travel[0]['origin_time']
        return datetime.strptime(nearest_time, "%m-%d-%y %H:%M:%S")

    def get_travel(self) -> list:
        # returns list with trips and their departures
        # return self.sl.get_trip()
        return self.sl_travel

    
    """ ### ToDo ### """
    def __TODO__(self):
        """ When access token is received, set standard list, timestamp & activate"""
        self.set_other_list("Inköpslista")
        self.todo_prev_time = self.get_current_time().strftime("%H:%M")
        self.todo_expires = self.todo.expires_in
        self.todo_active = True
        self.todo_refreshed = True

    def get_todo_auth(self) -> str:
        """ returns microsoft log in url for authentication """
        return self.todo.authorize()

    def set_auth(self, token) -> None:
        """ gets access token and sets authorization token"""
        self.todo.get_token(token)

    def refresh_auth_token(self) -> None:
        """ refreshing authorization token """
        self.todo.refresh_get_token()
        self.todo_expires = self.todo.expires_in

    def set_other_list(self, user_input:str) -> None:
        print("Sets new list inside (set_other_list)")
        self.todo_list = self.todo.return_tasks(user_input)
        
    def get_other_list(self, user_input:str) -> dict:
        print("Get new list inside (get_other_list)")
        self.todo_list = self.todo.return_tasks(user_input)
        return self.todo_list

    def get_list(self) -> dict:
        print("Gets new list inside (get_list)")
        self.todo_list = self.todo.return_tasks(self.todo_list["name"])
        return self.todo_list

    def get_expired_time(self) -> datetime:
        return self.todo.expires_in

    def add_new_task(self, task_input):
        print("Sets new list inside (add_new_task)")
        self.todo.add_task(task_input)


    """ ### FITBIT ### """
    def __FITBIT__(self):
        self.fitbit_list = self.set_sleep_summary()
        self.fitbit_active = True
        self.fitbit_refreshed = True

    def get_fitbit_auth(self) -> str:
        """ returns microsoft log in url for authentication """
        return self.fitbit.authorize()

    def set_fitbit_auth(self, code:str) -> None:
        self.fitbit.get_token(code)

    def set_sleep_summary(self):
        sleep_log = self.fitbit.get_sleep_summary()
        if (len(sleep_log) != 0):
            return sleep_log
        else:
            print("MOA had a problem with retrieving sleep log from fitbit")
            return None
            
    def get_sleep(self):
        return self.fitbit_list


    """     Weather     """
    def __WEATHER__(self, city:str):
        self.set_weather_new_location(city)
        self.weather_current = self.set_current_weather()
        self.weather_forecast = self.set_forecast_weather()

    def set_weather_new_location(self, city:str):
        self.weather_location = city
        self.weather.set_location(city)

    def set_current_weather(self) -> dict:
        current_weather = self.weather.set_current()
        if (current_weather != None):
            self.weather_current = current_weather
            print("New Weather data is set")
            return self.weather_current
        else:
            self.log_data("MOA WEATHER: ERROR - current_weather returned None")
            return {"temperature": "Error"}

    def set_forecast_weather(self) -> list:
        forecast_weather = self.weather.set_forecast()
        if (forecast_weather != None):
            self.weather_forecast = forecast_weather[:4]
            print("New forecast is set")
            return self.weather_forecast
        else:
            self.log_data("MOA WEATHER: ERROR - forecast_weater returned None")
            return {"temperature": "Error"}

    def get_current_weather(self):
        return self.weather_current

    def get_forecast_weather(self):
        return self.weather_forecast



    """ LOG DATA """
    def log_data(self, data:str) -> None:
        with open("log/logged.txt", "a") as file:
            dt = datetime.now().strftime("%m-%d-%y %H:%M:%S")
            log_file = f"[{dt}] - {data}\n"
            file.write(log_file)
            file.close()
        

    



if __name__ == "__main__":
    moa = MOA()