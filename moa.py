from API.SL_TRAFFIC.sl import SL
from API.WEATHER.weather import Weather
from API.HUE.hue import Hue


class MOA:

    def __init__(self) -> None:

        # API init
        self.SL = SL()
        self.weather = Weather()
        self.hue = Hue()

        self.set_trains("Vällingby", "Sankt Eriksplan")
        self.hue.print_all_lights()
        

    """     SL      """
    def set_trains(self, travel_org, travel_des):
        self.SL.set_transport(travel_org, travel_des)
        self.SL.create_transport()

    def refresh_trains(self):
        self.SL.create_transport()

    def get_trains(self):
        return self.SL.trains