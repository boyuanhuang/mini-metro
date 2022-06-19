import random

from config import STATION_FORMS, CUMUL_PROBA_STATION_FORMS, STATION_CAPACITY
from engine.util_functions import set_random_form
from passenger import Passenger
from engine.metroline import MetroLine
from config import MAP_LEVEL


class Map:

    def __init__(self):
        # Display
        self.map_level = 1
        self.metrolines: list[MetroLine] = None
        self.stations: list[Station] = []
        self.station_amount = 0
        self.waterzone = None

        # Timer and counter
        self.timer = None
        self.passenger_transported = 0

        # Tool
        # todo

    def display(self):
        pass

    def generate_station(self):
        self.station_amount += 1
        self.stations.append(Station(id_=self.station_amount, position=self.random_position()))

    def zoom_out(self):
        self.map_level += 1

    def random_position(self):
        max_height, max_width = MAP_LEVEL[self.map_level]
        position = (random.uniform(0, max_height), random.uniform(0, max_width))
        while position in self.waterzone:  # todo implement 'in' condition
            position = (random.uniform(0, max_height), random.uniform(0, max_width))
        return position


class Station:

    def __init__(self, id_, position):
        self.id = id_
        self.position = position
        self.form = set_random_form(STATION_FORMS, CUMUL_PROBA_STATION_FORMS)
        self.type = 'Normal'
        self.capacity = STATION_CAPACITY[self.type]
        self.timer = None
        self.passengers = []
        self.attached_metrolines = []
        self.next_stations = dict()  # ex : {1: Station1, 2: Station 2, ... }
        self.previous_stations = dict()  # ex : {1: Station1, 2: Station 2, ... }

    def create_passenger(self):
        self.passengers.append(Passenger())

    def onboard_passenger(self):
        return self.passengers.pop(0)

    def change_station_type(self, type_):
        self.type = type_
        self.capacity = STATION_CAPACITY[self.type]


if __name__ == '__main__':
    map = Map()
    print(1)
    print()
