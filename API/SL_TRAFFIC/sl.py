from API.api_keys import *
from datetime import datetime, timedelta
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
        self.transports = []
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
                with open("log/errors.txt", "a") as file:
                    dt = datetime.now().strftime("%m-%d-%y %H:%M:%S")
                    error_data = f"[{dt}] - {e} : {data}\n"
                    file.write(error_data)

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
        self.transports = []
        self.total_t = None

    def convert_datetime(self, date:str, time:str) -> datetime:
        year = date[2:4]
        month = date[5:7]
        day = date[8:10]
        date_time = f"{month}-{day}-{year} {time}"
        converted_date = datetime.strptime(date_time, "%m-%d-%y %H:%M:%S")
        return converted_date

    def create_transport_icon(self, product:dict) -> dict:

        name = product['name']
        category = product['catIn']
        color = ""

        # if category is pendeltåg
        if (category == "TRN"):
            color = "pink"

        # if category is tunnelbana
        elif (category == "MET"):
            if "grön" in name:
                color = "green"
            elif "röd" in name:
                color = "red"
            elif "blå" in name:
                color = "blue"
        
        elif (category == "BUS"):
            if "blå" in name:
                color = "blue"
            else:
                color = "red"

        else:
            color = "grey"

        transport = {
            "name" : name,
            "type" : category,
            "line" : product['line'],
            "color": color
        }
        return transport

    def set_trip(self) -> list:
        travel_url = f"https://api.sl.se/api2/TravelplannerV3_1/trip.json?key={SL_TRAVEL_KEY}"
        dt = (datetime.now() + timedelta(minutes=2)).strftime("%H:%M")
        # print(f"TIME NOW = {datetime.now()}")
        # print(f"TIME (dt) = {dt}")
        parameters = {
            "originId" : self.from_station["SiteId"],
            "destId" : self.to_station["SiteId"],
            "Time": dt
        }
        # get request with api url and search parameters
        response = requests.get(travel_url, params=parameters)
        print(f"set_trip API response : [{response.status_code}]")
        self.travel_trips = []
        # error handling
        if (response.status_code == 200):
            # with open("SL.json", "w") as file:
            #     file.write(response.text)
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
                            self.origin_t = self.convert_datetime(trip['Origin']['date'], trip['Origin']['time'])
                        
                        # if last transport in trip, set destination as destination
                        if (trip == trip_data["LegList"]["Leg"][-1]):
                            self.destin = destin_name
                            self.destin_t = self.convert_datetime(trip['Destination']['date'], trip['Destination']['time'])
                            total_time = str(self.destin_t - self.origin_t)
                            if (total_time[0] == '0'):
                                self.total_t = f"{total_time[2:4]} min"
                            else:
                                self.total_t = f"{total_time[:4]} tim"

                        # pass if transport is walk && its not first or last 
                        if (trip["type"] == "WALK"):
                            continue

                        # if transport changes necessary for trip, append stops in legs list
                        else:
                            
                            transport = self.create_transport_icon(trip['Product'])
                            self.transports.append(transport)
                            new_train = {
                                "origin_name": origin_name,
                                "origin_time": origin_time,
                                "destin_name": destin_name,
                                "destin_time": destin_time,
                                "transport": transport
                            }
                            self.legs.append(new_train)

                    # create travel object of trip and append to travel list
                    origin_time_str = self.origin_t.strftime("%m-%d-%y %H:%M:%S")
                    destin_time_str = self.destin_t.strftime("%m-%d-%y %H:%M:%S")
                    new_travel = {"origin_name": self.origin,
                                "origin_time": origin_time_str,
                                "destin_name": self.destin,
                                "destin_time": destin_time_str,
                                "total_time": self.total_t,
                                "changes": self.legs,
                                "transports": self.transports}
                    self.travel_trips.append(new_travel)

                # print(f"travel_trips array returned\nFirst departure: {self.travel_trips[0]['origin_time']}")
                return self.travel_trips
            
            except (TypeError, KeyError) as e:
                with open("log/errors.txt", "a") as file:
                    dt = datetime.now().strftime("%m-%d-%y %H:%M:%S")
                    error_data = f"[{dt}] - {e} : {data}\n"
                    file.write(error_data)                
                return self.travel_trips
        
        else:
            with open("log/errors.txt", "a") as file:
                dt = datetime.now().strftime("%m-%d-%y %H:%M:%S")
                error_data = f"[{dt}] - set_trip API response : [{response.status_code}]\n"
                file.write(error_data)
            return self.travel_trips

    def get_trip(self):
        return self.travel_trips


if __name__ == "__main__":
    sl = SL()  
    sl.get_every_station("Sankt Eriksplan")
    sl.get_every_station("Karolinska institutet västra")
    array = sl.set_trip()