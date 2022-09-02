class Transport():

    def __init__(self, name, transportType, line, transportSubType, distance, direction, operatorCode) -> None:
        self.name = name
        self.transportType = transportType
        self.line = line
        self.transportSubType = transportSubType
        self.distance = distance
        self.direction = direction
        self.operatorCode = operatorCode