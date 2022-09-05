from .sl_id import API_ID_DICT
from .sl_objects import SL_OBJECT

"""
SL_URL = Creates URL

takes input /
    * from station 
    * destination station 
    * how many choices 
    * arrival / departure date and time 

"""

class SL_URL():

    def __init__(self) -> None:
        self.URL = ""
        self.origPlaceId = ""
        self.destPlaceId = ""
        self.searchForArrival = False
        self.datetime = ""
        self.desiredResults = 0

    def getUTL(self):
        return self.URL

    def create_URL(self, o_name, d_name):
        self.URL = "https://webcloud.sl.se/v2/api/travels?mode=travelPlanner&"
        self.URL += f"origPlaceId={self.origPlaceId}&"
        self.URL += f"destPlaceId={self.destPlaceId}&"
        self.URL += f"searchForArrival={self.searchForArrival}&"
        self.URL += f"transportTypes=111&desiredResults={self.desiredResults}&"
        self.URL += f"origName={o_name}&destName={d_name}&"

    def train(self, origName, destName, desiredResults=20):
        self.origPlaceId = API_ID_DICT[origName]
        self.destPlaceId = API_ID_DICT[destName]
        self.desiredResults = desiredResults
        self.searchForArrival = False

        self.create_URL(origName, destName)
        return SL_OBJECT(self.URL)
    
    def trainDeparture(self, origName, destName, desiredResults, datetime):
        self.origPlaceId = API_ID_DICT[origName]
        self.destPlaceId = API_ID_DICT[destName]
        self.desiredResults = desiredResults
        self.searchForArrival = False
        self.datetime = datetime

        self.create_URL(origName, destName)
        self.URL += f"datetime={self.datetime}"
        return SL_OBJECT(self.URL)

    def trainArrival(self, origName, destName, desiredResults, datetime):
        self.origPlaceId = API_ID_DICT[origName]
        self.destPlaceId = API_ID_DICT[destName]
        self.desiredResults = desiredResults
        self.searchForArrival = True
        self.datetime = datetime

        self.create_URL(origName, destName)
        self.URL += f"datetime={self.datetime}"
        return SL_OBJECT(self.URL)
