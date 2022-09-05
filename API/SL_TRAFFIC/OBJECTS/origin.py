from .origin import Origin
from .destination import Destination
from .transport import Transport

class Legs():

    def __init__(self, origin : Origin, destination : Destination, intermediateStops, transport : Transport, durationSeconds, hidden):
        self.origin = origin
        self.destination = destination
        self.intermediateStops = intermediateStops
        self.transport = transport
        self.durationSeconds = durationSeconds
        self.hidden = hidden