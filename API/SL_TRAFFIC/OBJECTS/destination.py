class Destination():

    def __init__(self, name, arrivalTime_planned, arrivalTime_realTime, track, latitude, longitude) -> None:
        self.name = name 
        self.arrivalTime_planned = arrivalTime_planned
        self.arrivalTime_realTime = arrivalTime_realTime
        self.track = track 
        self.latitude = latitude
        self.longitude = longitude