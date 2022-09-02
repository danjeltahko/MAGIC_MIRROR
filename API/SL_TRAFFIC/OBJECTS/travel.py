from .destination import Destination
from .origin import Origin

class Travel():

    def __init__(self, origin : Origin, destination : Destination, durationSeconds, legs, isCongested, priceInfo, _links) -> None:
        self.origin = origin
        self.destination = destination
        self.durationSeconds = durationSeconds
        self.legs = legs
        self.isCongested = isCongested
        self.priceInfo = priceInfo
        self._links = _links

    def print_basic(self):

        for i in range(len(self.legs)):
            print("Departure : " + self.legs[i].origin.name)
            print("Time : " + self.legs[i].origin.departure_planned)
            print(f"-> {self.legs[i].transport.name}")
            print("Arrival : " + self.legs[i].destination.name)
            print(f"Time : {self.legs[i].destination.arrivalTime_planned} \n")

    def print_all_stops(self):

        for i in range(len(self.legs)):
            print("Departure : " + self.legs[i].origin.name)
            print("Time : " + self.legs[i].origin.departure_planned)
            print(f"-> {self.legs[i].transport.name}")
            for x in range(len(self.legs[i].intermediateStops)):
                print("Name : " + self.legs[i].intermediateStops[x].name)
                print("Arrival : " + self.legs[i].intermediateStops[x].arrivalTime_planned)

            print("Arrival : " + self.legs[i].destination.name)
            print(f"Time : {self.legs[i].destination.arrivalTime_planned} \n")