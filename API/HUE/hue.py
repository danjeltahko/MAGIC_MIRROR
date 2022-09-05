from phue import Bridge
from API.api_keys import *


# https://github.com/studioimaginaire/phue

class Hue:

    def __init__(self) -> None:

        self.light_1 = "Hue white lamp 1"
        self.light_2 = "Hue white lamp 2"
        self.light_3 = "Hue white lamp 3"
        self.light_4 = "Hue color lamp 1"
        self.light_5 = "Hue filament bulb 1"

        self.kitchen = [self.light_1, self.light_2]
        self.bedroom = [self.light_3]
        self.livingroom = [self.light_4, self.light_5]

        self.all_lights = [self.light_1, self.light_2, self.light_3,
                            self.light_4, self.light_5]

        self.bridge = Bridge(HUE_BRIDGE)
        self.bridge.connect()

    def print_all_lights(self):

        lights = self.bridge.lights
        for l in lights:
            print(l.name)

    def turn_off_all(self):
        self.bridge.set_light(self.all_lights, 'off')

    def turn_off_all(self):
        self.bridge.set_light(self.all_lights, 'on')