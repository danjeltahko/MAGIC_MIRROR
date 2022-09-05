from MODELS.sl_url import SL_URL

class SL:

    def __init__(self) -> None:
        self.trains = []
        self.travel_from = None 
        self.travel_to = None

    def get_transport(self, travel_from, travel_to):
        self.travel_from = travel_from 
        self.travel_to = travel_to

    def create_transport(self):
        
        url = SL_URL().create_URL()
        train = url.train(self.travel_from, self.travel_to)
        self.trains = train.createObjects()

        return 

        
    def refresh(self):
        

