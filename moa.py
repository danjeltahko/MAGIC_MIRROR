from API import Aftonbladet, CoinMarketCap, Hue, SL, Trakt, Weather, Fitbit, ToDo
from DATABASE.aws import AWS
from datetime import datetime, timedelta
import pandas as pd
import requests, json

__version__ = 1.0
__author__ = 'https://github.com/DanjelTahko'

class MOA:

    """ Mamma & Assistent """

    def __init__(self) -> None:

        # Time & Date init
        self.current_time = "00:00:00"
        self.current_day = "Sön 20 Apr"
        self.minute_time = "00:00"

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
        self.__WEATHER__(self.weather_location)

        # ToDo init
        self.todo = ToDo()
        self.todo_list = {"name": None}
        self.todo_active = False
        self.todo_refreshed = False
        self.todo_refreshed_user = False
        self.todo_expires = None

        # Fitbit init
        self.fitbit = Fitbit()
        self.fitbit_list = {}
        self.fitbit_active = False
        self.fitbit_refreshed = False
        self.fitbit_expires = None

        # SOIL SENSOR
        self.aws_db = AWS()
        self.aws_db_data = None
        self.last_waterplant = None
        self.aws_refreshed = False
        self.set_AWS()
        #The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all(). ?????

        # Philips HUE
        self.hue = Hue()

        # self.news = Aftonbladet()

        # General init
        self.connected = 0

    def HUE_connect(self):
        connecting = self.hue.connect()
        if (connecting):
            print("CONNECTED")
        else:
            print("FAILED TO CONNECT")

    def HUE_OFF(self):
        self.hue.turn_lights_off()
    
    def HUE_ON(self):
        self.hue.turn_lights_on()




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
        self.log_data(f"MOA SL : SL __init__ ")
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
        self.log_data(f"MOA SL : new 'travel_from' is set to {self.sl.from_station['Name']}")

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
        self.log_data(f"MOA SL : new 'travel_to' is set to {self.sl.to_station['Name']}")

    def set_new_travel(self) -> None:
        """ Creates travel dictionary list with travel data """
        self.log_data(f"MOA SL : Trying to create new travel data from API")
        # sets trip to destination with next 5 departures
        self.sl_travel = self.sl.set_trip()
        if (len(self.sl_travel) > 0):
            self.sl_new = True
            self.log_data("MOA SL : Successfully created new Travel with new train departures")
        else:
            self.log_data("MOA SL : Failed to created new Travel with new trains and departures. (See ERROR for more info)")

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
    def get_todo_auth(self) -> str:
        """ returns microsoft log in url for authentication """
        self.log_data("MOA TODO : Creating URL for Microsoft TODO to receive access token")
        return self.todo.authorize()

    def set_todo_auth(self, token) -> None:
        """ gets access token and sets authorization token"""
        self.log_data("MOA TODO : Trying to received access token from https://login.microsoftonline.com/common/oauth2/v2.0/token with retrieved code token")
        auth = self.todo.get_token(token)
        if (auth):
            self.log_data("MOA TODO : Successfully received access token")
            self.todo_expires = self.todo.expires_in
            self.todo_active = True
        else:
            self.log_data("[ERROR] MOA TODO : Failed to received access token")
            self.todo_active = False

    def todo_refresh_auth_token(self) -> None:
        """ refreshing authorization token """
        self.log_data("MOA TODO : Trying to refresh access token from https://login.microsoftonline.com/common/oauth2/v2.0/token")
        auth = self.todo.refresh_get_token()
        if (auth):
            self.log_data("MOA TODO : Successfully refreshed access token")
            self.todo_expires = self.todo.expires_in
        else:
            self.log_data("[ERROR] MOA TODO : Failed to refreshed access token")
            self.fitbit_active = False

    def get_list(self) -> dict:
        """ returns dictionary with task from todo list """
        self.todo_list = self.todo.return_tasks(self.todo_list["name"])
        if (self.todo_list["name"] != "ERROR"):
            self.log_data(f"MOA TODO : Successfully received tasks from {self.todo_list['name']} list")
            if (not self.todo_active):
                self.todo_active = True
        else:
            self.log_data(f"[ERROR] MOA TODO : Failed to received tasks from {self.todo_list['name']} list")
            self.todo_active = False
        
        return self.todo_list

    def add_new_task(self, task_input) -> None:
        """ Try to add new task to todo list"""
        self.log_data(f"MOA TODO : Trying to add a new task to {self.todo_list['name']} list")
        success = self.todo.add_task(task_input)
        if (success):
            self.log_data(f"MOA TODO : Successfully added '{task_input}' task to {self.todo_list['name']} list")
            if (not self.todo_active):
                self.todo_active = True
        else:
            self.log_data(f"[ERROR] MOA TODO : Failed to add '{task_input}' task to {self.todo_list['name']} list")
            self.todo_active = False


    """ ### FITBIT ### """
    def get_fitbit_auth(self) -> str:
        """ returns todo url for authentication """
        self.log_data("MOA FITBIT : Creating URL for fitbit to receive access token")
        return self.fitbit.authorize()

    def set_fitbit_auth(self, code:str) -> None:
        """ making get request for access token with given code from auth url"""
        self.log_data("MOA FITBIT : Trying to received access token from https://api.fitbit.com/oauth2/token with retrieved code token")
        auth = self.fitbit.get_token(code)
        if (auth):
            self.log_data("MOA FITBIT : Successfully received access token")
            self.fitbit_expires = self.fitbit.expires_in
            self.fitbit_active = True
        else:
            self.log_data("[ERROR] MOA FITBIT : Failed to received access token")
            self.fitbit_active = False

    def fitbit_refresh_auth_token(self) -> None:
        """ refreshing authorization token """
        self.log_data("MOA FITBIT : Trying to refresh access token from https://www.fitbit.com/oauth2/authorize")
        auth = self.todo.refresh_get_token()
        if (auth):
            self.log_data("MOA FITBIT : Successfully refreshed access token")
            self.todo_expires = self.todo.expires_in
        else:
            self.log_data("[ERROR] MOA FITBIT : Failed to refreshed access token")
            self.fitbit_active = False

    def set_sleep_summary(self) -> dict:
        self.log_data("MOA FITBIT : Trying to get Sleep Data from API")
        self.fitbit_list = self.fitbit.get_sleep_summary()
        if (self.fitbit_list["summary"] != "ERROR"):
            self.log_data("MOA FITBIT : Successfully received new Sleep Data from API")
            if (not self.fitbit_active):
                self.fitbit_active = True
        else:
            self.log_data("[ERROR] MOA FITBIT : Failed to received new Sleep Data from API")
            self.fitbit_active = False
        
        return self.fitbit_list
            

    """     Weather     """
    def __WEATHER__(self, city:str) -> None:
        """ weather init """
        self.set_weather_new_location(city)
        self.weather_current = self.set_current_weather()
        self.weather_forecast = self.set_forecast_weather()

    def set_weather_new_location(self, city:str) -> None:
        """ sets new weather location """
        self.weather_location = city
        success = self.weather.set_location(city)
        if (success):
            self.log_data(f"MOA WEATHER : Successfully set weather to {city}")
        else:
            self.log_data(f"[ERROR] MOA WEATHER : Successfully set weather to {city}")

    def set_current_weather(self) -> dict:
        """ gets new current weather data"""
        self.log_data("MOA WEATHER : Trying to get current weather data from API")
        current_weather = self.weather.set_current()
        if (current_weather != None):
            self.weather_current = current_weather
            self.log_data(f"MOA WEATHER : Successfully received new weather data")
            return self.weather_current
        else:
            self.log_data("[ERROR] MOA WEATHER : Failed to receive current_weather data")
            return {"temperature": "ERROR"}

    def set_forecast_weather(self) -> list:
        """ gets new weather forecast data"""
        self.log_data("MOA WEATHER : Trying to get weather forecast data from API")
        forecast_weather = self.weather.set_forecast()
        if (forecast_weather != None):
            # returns only first 4 weather objects
            self.weather_forecast = forecast_weather[:4]
            self.log_data(f"MOA WEATHER : Successfully received new weather forecast data")
            return self.weather_forecast
        else:
            self.log_data(f"[ERROR] MOA WEATHER : Failed to received new weather forecast data")
            return [{"temperature": "ERROR"}]

    def get_nearest_weather_time(self) -> datetime:
        """ Returns first weather date in list: 01-23-2022 22:50:30 """
        nearest_time = self.weather_forecast[0]['dt']
        return datetime.strptime(nearest_time, "%m-%d-%y %H:%M:%S")


    """ AWS Dynamo DB """
    def set_AWS(self) -> None :
        self.set_new_AWS_data()
        self.set_last_AWS_data()

    def set_new_AWS_data(self) -> None:
        self.log_data(f"MOA WATERPLANT : Trying to get data from AWS Dynamo DB")
        self.aws_db_data = self.aws_db.get_data_waterplant()
        if (not self.aws_db_data.empty):
            self.log_data(f"MOA WATERPLANT : Successfully received data from database")
        else:
            self.log_data(f"MOA WATERPLANT : Failed to received data from database")

    def get_AWS_data(self) -> pd.DataFrame:
        return self.aws_db_data

    def set_last_AWS_data(self) -> None:
        self.last_waterplant = {"date": self.aws_db_data.iloc[-1]["Datetime"], "moist": int(self.aws_db_data.iloc[-1]["Moisture"])}

    def get_last_AWS_data(self) -> dict:
        return self.last_waterplant
    
    def get_next_AWS_date(self):
        time_stamp = self.get_last_AWS_data()
        next_time = time_stamp["date"]
        next_time = (next_time + timedelta(minutes=31))
        return next_time


    """ LOG DATA """
    def log_data(self, data:str) -> None:
        """ logs everything to file! """
        with open("log/logged.txt", "a") as file:
            dt = datetime.now().strftime("%m-%d-%y %H:%M:%S")
            log_file = f"[{dt}] - {data}\n"
            file.write(log_file)

    def get_logged_data(self, date_start:str=None, date_end:str=None, time_start:str=None, time_end:str=None) -> list[str]:
        """ returns logs with given parameters or all """
        try:
            new_logged_data_list = []
            with open("log/logged.txt", "r") as file:
                logged_lines = file.readlines()

                # if no input were given, set default value
                if (date_start == None):
                    date_start = "01-01-23"
                if (time_start == None):
                    time_start = "00:00"
                if (date_end == None):
                    date_end = datetime.now().strftime("%m-%d-%y")
                if (time_end == None):
                    time_end = datetime.now().strftime("%H:%M")
                
                # converts input to datetime objects
                start = datetime.strptime(f"{date_start} {time_start}", "%m-%d-%y %H:%M")
                end = datetime.strptime(f"{date_end} {time_end}", "%m-%d-%y %H:%M")

                for line in logged_lines:
                    # converts every logged date to datetime object
                    line_dt = datetime.strptime(line[1:15], "%m-%d-%y %H:%M")
                    # if logged data is between input datetime
                    if (line_dt >= start and line_dt <= end):
                        # add to new list which will be returned
                        new_logged_data_list.append(line)

                return new_logged_data_list

        except ValueError as e:
            return [e]
        

if __name__ == "__main__":
    moa = MOA()