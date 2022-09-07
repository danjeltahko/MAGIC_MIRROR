from API.WEATHER.weather_api import Weather_API
from datetime import datetime

class Weather(Weather_API):

    def __init__(self) -> None:
        super().__init__()        
        self.current_temp = None
        self.forecast = []

    
    def convert_delta(self, dt):
        ts = int(dt)


    def create_MM_forecast(self):
        pass
        #self.forecast = self.set_forecast()
        #self.current_temp = self.set_current_weather()




    def refresh(self):
        self.current_temp = self.set_current_weather()


    