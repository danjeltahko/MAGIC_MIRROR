from API.api_keys import *
from API.SL_TRAFFIC.train import Train
from API.SL_TRAFFIC.travel import Travel
from datetime import datetime 
import requests 
import json

class SL:

    def __init__(self) -> None:

        self.from_station = None
        self.to_station = None
        self.travel_trips = []

        # travel template
        self.origin = None
        self.destin = None
        self.origin_t = None
        self.destin_t = None
        self.legs = []
        self.total_t = None

    def get_every_station(self, station:str) -> list[dict]:
        """ returns list dictionaries with stations similar to search station """
        search_url = f"https://api.sl.se/api2/typeahead.json?key={SL_STATION_KEY}&searchstring={station}"
        response = requests.get(search_url)
        print(f"get_stations[{response.status_code}] -> {station}")
        if (response.status_code == 200):
            data = json.loads(response.text)
            try:
                return data["ResponseData"]
            except KeyError as e:
                print(e)
                print(data)
                print("\n")

    def get_station_id(self, stations:list, index:int) -> dict:
        """ returns dictionary at list index input: name, id and type. """
        return stations[index]

    def set_from_station(self, station_from:dict) -> None:
        """ sets departure station """
        self.from_station = station_from

    def set_to_station(self, station_to:dict) -> None:
        """ sets destination station"""
        self.to_station = station_to

    def reset_template(self) -> None:
        """ restes template from Travel class """
        self.origin = None
        self.destin = None
        self.origin_t = None
        self.destin_t = None
        self.legs = []
        self.total_t = None

    def set_trip(self) -> list:
        travel_url = f"https://api.sl.se/api2/TravelplannerV3_1/trip.json?key={SL_TRAVEL_KEY}"
        parameters = {
            "originId" : self.from_station["SiteId"],
            "destId" : self.to_station["SiteId"]
        }
        # get request with api url and search parameters
        response = requests.get(travel_url, params=parameters)
        print(f"test_travel : [{response.status_code}]")
        self.travel_trips = []
        # error handling
        if (response.status_code == 200):
            data = json.loads(response.text)
            # loops through every departure
            try:
                for trip_data in data["Trip"]:
                    # loops through every transportation
                    self.reset_template()
                    for trip in trip_data["LegList"]["Leg"]:
                        
                        origin_name = trip['Origin']['name']
                        origin_time = trip['Origin']['time']
                        destin_name = trip['Destination']['name']
                        destin_time = trip['Destination']['time']
                        transport = trip['name']
                        
                        # if first transport in trip, set origin as origin
                        if (trip == trip_data["LegList"]["Leg"][0]):
                            self.origin = origin_name
                            self.origin_t = datetime.strptime(trip['Origin']['time'], '%H:%M:%S')
                        
                        # if last transport in trip, set destination as destination
                        if (trip == trip_data["LegList"]["Leg"][-1]):
                            self.destin = destin_name
                            self.destin_t = datetime.strptime(trip['Destination']['time'], '%H:%M:%S')
                            self.total_t = self.destin_t - self.origin_t

                        # if transport changes necessary for trip, append stops in legs list
                        else:
                            new_train = {"origin_name": origin_name,
                                        "destin_name": destin_name,
                                        "transport": transport,
                                        "origin_time": origin_time,
                                        "destin_time": destin_time}
                            self.legs.append(new_train)

                    # create travel object of trip and append to travel list
                    origin_time_str = self.origin_t.strftime('%H:%M:%S')
                    destin_time_str = self.destin_t.strftime('%H:%M:%S')
                    new_travel = {"origin_name": self.origin,
                                "origin_time": origin_time_str,
                                "destin_name": self.destin,
                                "destin_time": destin_time_str,
                                "changes": self.legs}
                    self.travel_trips.append(new_travel)

                return self.travel_trips
            
            except TypeError as e:
                print(e)
                print(data)
        
        else:
            return self.travel_trips

    def get_trip(self):
        return self.travel_trips


    def print_trains(self, array):
        """ prints out everything, for testing purpose """
        for travel in array:
            print(f"Origin {travel.origin_t} -> {travel.origin}")
            print(f"Destin {travel.destin_t} -> {travel.destin}")
            print(f"Legs : {len(travel.legs)}")
            print(f"Total time : {travel.total_t}")
            print("---------------------------")




if __name__ == "__main__":
    sl = SL()  
    #sl.set_to_station("Sankt Eriksplan")
    sl.set_to_station("Karolinska institutet västra")
    array = sl.get_travel()
    sl.print_trains(array)
    #print(sl.get_from_station())

