import requests
import json

from API.SL_TRAFFIC.OBJECTS.destination import Destination
from API.SL_TRAFFIC.OBJECTS.origin import Origin
from API.SL_TRAFFIC.OBJECTS.transport import Transport
from API.SL_TRAFFIC.OBJECTS.intermediateStops import IntermediateStops
from API.SL_TRAFFIC.OBJECTS.priceInfo import PriceInfo
from API.SL_TRAFFIC.OBJECTS.legs import Legs
from API.SL_TRAFFIC.OBJECTS.travel import Travel

"""
SL_JSONL = Creates objects of travels

takes input /
    * url 

"""

class SL_OBJECT():

    def __init__(self, url) -> None:
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'}
        self.URL = url
        self.travels = []  # Array with Travel objects

    def createObjects(self):
        
        # response from url request
        response = requests.get(self.URL, headers=self.headers)
        # response in str
        data = response.text 
        # convert to dict
        jsonObject = json.loads(data)
        # iterate through every travel (desired results)
        for i in range(len(jsonObject["travels"])):
            
            # origin
            origin_name = jsonObject["travels"][i]["origin"]["name"]
            origin_departureTime_planned = jsonObject["travels"][i]["origin"]["departureTime"]["planned"]
            origin_departureTime_realTime = jsonObject["travels"][i]["origin"]["departureTime"]["realTime"]
            origin_track = jsonObject["travels"][i]["origin"]["track"]
            origin_coordinates_latitude = jsonObject["travels"][i]["origin"]["coordinates"]["latitude"]
            origin_coordinates_longitude = jsonObject["travels"][i]["origin"]["coordinates"]["longitude"]

            # create object of origin
            _origin = Origin(origin_name,
                            origin_departureTime_planned,
                            origin_departureTime_realTime,
                            origin_track,
                            origin_coordinates_latitude,
                            origin_coordinates_longitude)

            # destination
            destination_name = jsonObject["travels"][i]["destination"]["name"]
            destination_arrivalTime_planned = jsonObject["travels"][i]["destination"]["arrivalTime"]["planned"]
            destination_arrivalTime_realTime = jsonObject["travels"][i]["destination"]["arrivalTime"]["realTime"]
            destination_track = jsonObject["travels"][i]["destination"]["track"]
            destination_coordinates_latitude = jsonObject["travels"][i]["destination"]["coordinates"]["latitude"]
            destination_coordinates_longitude = jsonObject["travels"][i]["destination"]["coordinates"]["longitude"]

            # create object of destination
            _destination = Destination(destination_name,
                                        destination_arrivalTime_planned,
                                        destination_arrivalTime_realTime,
                                        destination_track,
                                        destination_coordinates_latitude,
                                        destination_coordinates_longitude)
            # durationSeconds
            _durationSeconds = jsonObject["travels"][i]["durationSeconds"]
            
            # legs
            _legs = []
            for y in range(len(jsonObject["travels"][i]["legs"])):
                
                # legs : origin (same as origin)
                legs_origin_name = jsonObject["travels"][i]["legs"][y]["origin"]["name"]
                legs_origin_departureTime_planned = jsonObject["travels"][i]["legs"][y]["origin"]["departureTime"]["planned"]
                legs_origin_departureTime_realTime = jsonObject["travels"][i]["legs"][y]["origin"]["departureTime"]["realTime"]
                legs_origin_track = jsonObject["travels"][i]["legs"][y]["origin"]["track"]
                legs_origin_coordinates_latitude = jsonObject["travels"][i]["legs"][y]["origin"]["coordinates"]["latitude"]
                legs_origin_coordinates_longitude = jsonObject["travels"][i]["legs"][y]["origin"]["coordinates"]["longitude"]
                
                # create object of origin 
                _legs_origin = Origin(legs_origin_name,
                                    legs_origin_departureTime_planned,
                                    legs_origin_departureTime_realTime,
                                    legs_origin_track,
                                    legs_origin_coordinates_latitude,
                                    legs_origin_coordinates_longitude)

                # legs : destination (same as destination)
                legs_destination_name = jsonObject["travels"][i]["legs"][y]["destination"]["name"]
                legs_destination_arrivalTime_planned = jsonObject["travels"][i]["legs"][y]["destination"]["arrivalTime"]["planned"]
                legs_destination_arrivalTime_realTime = jsonObject["travels"][i]["legs"][y]["destination"]["arrivalTime"]["realTime"]
                legs_destination_track = jsonObject["travels"][i]["legs"][y]["destination"]["track"]
                legs_destination_coordinates_latitude = jsonObject["travels"][i]["legs"][y]["destination"]["coordinates"]["latitude"]
                legs_destination_coordinates_longitude = jsonObject["travels"][i]["legs"][y]["destination"]["coordinates"]["longitude"]
                
                # create object of destination
                _legs_destination = Destination(legs_destination_name,
                                            legs_destination_arrivalTime_planned,
                                            legs_destination_arrivalTime_realTime,
                                            legs_destination_track,
                                            legs_destination_coordinates_latitude,
                                            legs_destination_coordinates_longitude)
                # intermediateStops
                _intermediateStops = []
                for x in range(len(jsonObject["travels"][i]["legs"][y]["intermediateStops"])):

                    intermediateStops_name = jsonObject["travels"][i]["legs"][y]["intermediateStops"][x]["name"]
                    intermediateStops_departureTime_planned = jsonObject["travels"][i]["legs"][y]["intermediateStops"][x]["departureTime"]["planned"]
                    intermediateStops_departureTime_realTime = jsonObject["travels"][i]["legs"][y]["intermediateStops"][x]["departureTime"]["realTime"]
                    intermediateStops_arrivalTime_planned = jsonObject["travels"][i]["legs"][y]["intermediateStops"][x]["arrivalTime"]["planned"]
                    intermediateStops_arrivalTime_realTime = jsonObject["travels"][i]["legs"][y]["intermediateStops"][x]["arrivalTime"]["realTime"]
                    intermediateStops_coordinates_latitude = jsonObject["travels"][i]["legs"][y]["intermediateStops"][x]["coordinates"]["latitude"]
                    intermediateStops_coordinates_longitude = jsonObject["travels"][i]["legs"][y]["intermediateStops"][x]["coordinates"]["longitude"]

                    # create object of every intermediate stop
                    new_intermediateStops = IntermediateStops(intermediateStops_name,
                                                            intermediateStops_departureTime_planned,
                                                            intermediateStops_departureTime_realTime,
                                                            intermediateStops_arrivalTime_planned,
                                                            intermediateStops_arrivalTime_realTime,
                                                            intermediateStops_coordinates_latitude,
                                                            intermediateStops_coordinates_longitude)

                    # append it to array with every intermediate stop
                    _intermediateStops.append(new_intermediateStops)

            
                # transport
                transport_name = jsonObject["travels"][i]["legs"][y]["transport"]["name"]
                transportType = jsonObject["travels"][i]["legs"][y]["transport"]["transportType"]
                transport_line = jsonObject["travels"][i]["legs"][y]["transport"]["line"]
                transport_transportSubType = jsonObject["travels"][i]["legs"][y]["transport"]["transportSubType"]
                transport_distance = jsonObject["travels"][i]["legs"][y]["transport"]["distance"]
                transport_direction = jsonObject["travels"][i]["legs"][y]["transport"]["direction"]
                transport_operatorCode = jsonObject["travels"][i]["legs"][y]["transport"]["operatorCode"]

                # create object of transport
                _legs_transport = Transport(transport_name,
                                        transportType,
                                        transport_line,
                                        transport_transportSubType,
                                        transport_distance,
                                        transport_direction,
                                        transport_operatorCode)

                # durationSeconds
                _legs_durationSeconds = jsonObject["travels"][i]["legs"][y]["durationSeconds"]

                # hidden
                _legs_hidden = jsonObject["travels"][i]["legs"][y]["hidden"]

                LEGS = Legs(_legs_origin,
                            _legs_destination,
                            _intermediateStops,
                            _legs_transport,
                            _legs_durationSeconds,
                            _legs_hidden)
                
                _legs.append(LEGS)
            

            # isCongested
            _isCongested = jsonObject["travels"][i]["isCongested"]
            
            # priceInfo
            _priceInfo = []
            for z in range(len(jsonObject["travels"][i]["priceInfo"])):
                priceInfo_title = jsonObject["travels"][i]["priceInfo"][z]["title"]
                priceInfo_priceInfoType = jsonObject["travels"][i]["priceInfo"][z]["priceInfoType"]
                priceInfo_fullePrice = jsonObject["travels"][i]["priceInfo"][z]["fullPrice"]
                priceInfo_reducedPrice = jsonObject["travels"][i]["priceInfo"][z]["reducedPrice"]

                # create object of priceInfo
                new_priceInfo = PriceInfo(priceInfo_title,
                                        priceInfo_priceInfoType,
                                        priceInfo_fullePrice,
                                        priceInfo_reducedPrice)                    
                _priceInfo.append(new_priceInfo)

            # links
            _links = jsonObject["travels"][i]["_links"]["self"]

            TRAVEL = Travel(_origin,
                            _destination,
                            _durationSeconds,
                            _legs,
                            _isCongested,
                            _priceInfo,
                            _links)

            self.travels.append(TRAVEL)

        return self.travels
            