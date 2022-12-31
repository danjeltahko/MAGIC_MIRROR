class Train:
    def __init__(self, name, departure_planned, transport_name, destination_name, arrivaltime_planned) -> None:
        self.name = name 
        self.departure_planned = departure_planned
        self.transport_name = transport_name
        self.destination_name = destination_name
        self.arrivaltime_planned = arrivaltime_planned