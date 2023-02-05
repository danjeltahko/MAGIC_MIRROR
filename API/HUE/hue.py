from phue import Bridge
from API.api_keys import *


# https://github.com/studioimaginaire/phue

class Hue:

    def __init__(self) -> None:

        self.all_lights = ["Hue white lamp 1", "Hue white lamp 2",
                           "Hue white lamp 3", "Hue color lamp 1",
                           "Hue filament bulb 1", "Hue filament bulb 2",
                           "Hue color lamp 2", "Hue color lamp 3"]

        self.bridge = Bridge(ip=HUE_BRIDGE)

    def connect(self):
        try:
            self.bridge.connect()
            return True
        except Exception as e:
            print(e)            
            return False

    def turn_lights_off(self):
        self.bridge.set_light(self.all_lights, 'on', False)

    def turn_lights_on(self):
        self.bridge.set_light(self.all_lights, 'on', True)