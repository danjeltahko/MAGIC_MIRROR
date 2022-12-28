

class Train:

    def __init__(self, from_station, to_station, transport_name, departure_planed, departure_real, arrival_planned, arrival_real, date) -> None:
        
        self.from_station = from_station
        self.to_station = to_station
        self.transport_name = transport_name
        self.departure_planned = departure_planed
        self.departure_real = departure_real
        self.arrival_planned = arrival_planned
        self.arrival_real = arrival_real
        self.date = date