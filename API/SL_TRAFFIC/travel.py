from datetime import datetime

class Travel:

    def __init__(self, origin:str, origin_t:datetime, destin:str, destin_t, total_t:datetime, legs:list) -> None:
        self.origin = origin
        self.destin = destin
        self.origin_t = origin_t
        self.destin_t = destin_t
        self.legs = legs
        self.total_t = total_t