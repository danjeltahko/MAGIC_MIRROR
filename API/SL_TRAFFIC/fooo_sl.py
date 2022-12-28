from API.api_keys import *
from train import Train
import requests 
import json


from_station = "Sankt Eriksplan"
to_station = "Sankt Eriksplan"
url = f"https://api.sl.se/api2/TravelplannerV3_1/trip.json?key={SL_TRAVEL_KEY}"

#search = f"https://api.sl.se/api2/typeahead.json?key={api_key}&searchstring={from_station}&stationsonly=<ENDAST STATIONER>&maxresults<MAX ANTAL SVAR>"

class SL:

    def __init__(self) -> None:
        self.from_station = None
        self.to_station = None
        self.travel_info = None

    def get_station_id(self, station:str):
        """ returns first dictionary from stations array with Name and SiteId"""
        search_url = f"https://api.sl.se/api2/typeahead.json?key={SL_STATION_KEY}&searchstring={station}"
        response = requests.get(search_url)
        print(f"get station : [{response.status_code}]")
        if (response.status_code == 200):
            data = json.loads(response.text)
            return data["ResponseData"][0]

    def get_travel(self):
        travel_url = f"https://api.sl.se/api2/TravelplannerV3_1/trip.json?key={SL_TRAVEL_KEY}"
        parameters = {
            "originId" : self.from_station["SiteId"],
            "destId" : self.to_station["SiteId"]
        }
        response = requests.get(travel_url, params=parameters)
        print(f"get travel : [{response.status_code}]")
        print(response.text)
        if (response.status_code == 200):
            data = json.loads(response.text)
            train_array = []
            for trip in data["Trip"]:
                for train in trip["LegList"]["Leg"]:
                    from_station = train["Origin"]["name"]
                    departure_planned = train["Origin"]["time"]
                    if ("rtTime" in train["Origin"]):
                        departure_real = train["Origin"]["rtTime"]
                    else:
                        departure_real = None
                    to_station = train["Destination"]["name"]
                    arrival_planned = train["Destination"]["time"]
                    if ("rtTime" in train["Destination"]):
                        arrival_real = train["Destination"]["rtTime"]
                    else:
                        arrival_real = None
                    date = train["Destination"]["date"]
                    transport_name = train["name"]

                    new_train = Train(from_station,
                                        to_station,
                                        transport_name,
                                        departure_planned,
                                        departure_real,
                                        arrival_planned,
                                        arrival_real,
                                        date)
                    train_array.append(new_train)

            return train_array

        else:
            return []

    def print_trains(self, array):

        for data in array:
            print("---------------")
            print(data.from_station)
            print(f" -> {data.departure_planned}")
            print(data.to_station)
            print(f" -> {data.arrival_planned}")


        
                    
                    




    def set_from_station(self, station_from:str) -> None:
        self.from_station = self.get_station_id(station_from)

    def set_to_station(self, station_to:str) -> None:
        self.to_station = self.get_station_id(station_to)
    
    def set_both_stationsl(self, station_from:str, station_to:str) -> None:
        self.from_station = self.get_station_id(station_from)
        self.to_station = self.get_station_id(station_to)

    def get_from_station(self):
        return self.from_station

    def update(self):
        pass



sl = SL()            
sl.set_from_station("Vällingby")
#sl.set_to_station("Sankt Eriksplan")
sl.set_to_station("Karolinska institutet västra")
array = sl.get_travel()
sl.print_trains(array)
#print(sl.get_from_station())




#response = requests.get(search, headers=headers, params=parameters)

#print(response)
#print(response.text)

