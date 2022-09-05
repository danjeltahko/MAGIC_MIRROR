from API.SL_TRAFFIC.MODELS.sl_url import SL_URL
from API.SL_TRAFFIC.OBJECTS.train import Train

class SL:

    def __init__(self) -> None:
        self.trains = []
        self.travel_from = None 
        self.travel_to = None

    def set_transport(self, travel_from, travel_to):
        self.travel_from = travel_from 
        self.travel_to = travel_to

    def create_transport(self):
        
        train = SL_URL().train(self.travel_from, self.travel_to)
        travels = train.createObjects()

        # Simplified travel info..
        for travel in travels:
            for i in range(len(travel.legs)):
                name = travel.legs[i].origin.name
                departure = travel.legs[i].origin.departure_planned.split('T')[1][:-4]
                transport_name = travel.legs[i].transport.name
                destination_name = travel.legs[i].destination.name
                arrivaltime_planned = travel.legs[i].destination.arrivalTime_planned.split('T')[1][:-4]
                foo = Train(name, departure, transport_name, destination_name, arrivaltime_planned)
                self.trains.append(foo)

        return self.trains

    
        

