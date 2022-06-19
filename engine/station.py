from config import STATION_FORMS, CUMUL_PROBA_STATION_FORMS
from engine.tool_functions import set_random_form
from passenger import Passenger


class Station:

    def __init__(self, number):
        self.number = number
        self.position = (None, None)
        self.form = set_random_form(STATION_FORMS, CUMUL_PROBA_STATION_FORMS)

        self.passengers = []
        self.attached_metrolines = []
        self.next_stations = dict()  # ex : {1: Station1, 2: Station 2, ... }
        self.previous_stations = dict()  # ex : {1: Station1, 2: Station 2, ... }

    def create_passenger(self):
        self.passengers.append(Passenger())

    def onboard_passenger(self):
        return self.passengers.pop(0)
