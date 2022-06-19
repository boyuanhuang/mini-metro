import random

import config
from engine.util_functions import set_random_form
from engine.passenger import Passenger


class Map:

    def __init__(self):
        # Display
        self.map_level = 1
        self.metrolines: list[MetroLine] = []
        self.stations: dict = {}  # {station_id: Station}
        self.station_amount = 0
        self.waterzone = config.WATERZONE

        # Timer and counter
        self.timer = None
        self.passenger_transported = 0

        # Tool
        # todo

    def display(self):
        pass

    def generate_station(self):
        self.station_amount += 1
        self.stations[self.station_amount] = Station(station_id=self.station_amount, position=self.random_position())

    def zoom_out(self):
        self.map_level += 1

    def random_position(self):
        max_x, max_y = config.MAP_LEVEL[self.map_level]
        position = (random.uniform(0, max_x), random.uniform(0, max_y))
        while position in self.waterzone:  # todo implement 'in' condition
            position = (random.uniform(0, max_x), random.uniform(0, max_y))
        return position

    def get_station(self, id):
        return self.stations[id]


class Station(Map):

    def __init__(self, station_id, position):
        super().__init__()
        self.station_id = station_id
        self.position = position
        self.form = set_random_form(config.STATION_FORMS, config.CUMUL_PROBA_STATION_FORMS)
        self.type = 'Normal'
        self.capacity = config.STATION_CAPACITY[self.type]
        self.timer = None
        self.passengers = []
        self.attached_metrolines = []
        self.next_stations = dict()  # {metroline_id: Station_id}
        self.previous_stations = dict()  # {metroline_id: Station_id}

    def create_passenger(self):
        self.passengers.append(Passenger())

    def onboard_passenger(self):
        return self.passengers.pop(0)

    def change_station_type(self, type_):
        self.type = type_
        self.capacity = config.STATION_CAPACITY[self.type]


class MetroLine(Map):

    def __init__(self):
        super().__init__()
        self.metroline_id = None
        self.head_station_id: int = -1
        self.end_station_id: int = -1
        self.is_circular = (self.head_station_id == self.end_station_id)  # may be not useful ??

        self.stations = []  # [stations id]

        # Trains on this Metroline
        self.trains = []  # [Train1, Train2, ...]

    def extend_head_to(self, station_id):
        # Update connected Station's properties :
        connected_station = self.get_station(station_id)
        connected_station.next_stations[self.metroline_id] = self.stations[0]
        # Update stations list
        self.stations = [station_id] + self.stations

    def extend_end_to(self, station_id):
        # Update connected Station's properties :
        connected_station = self.get_station(station_id)
        connected_station.previous_stations[self.metroline_id] = self.stations[0]
        # Update stations list
        self.stations = [station_id] + self.stations

    def remove_station(self, station_id):
        # Update connected Station's properties :
        station_to_remove = self.get_station(station_id)

        flag_is_middle = True

        if station_id == self.head_station_id:
            del station_to_remove.next_stations[self.metroline_id]
            self.stations.remove(station_id)
            flag_is_middle = False

        if station_id == self.end_station_id:
            del station_to_remove.previous_stations[self.metroline_id]
            self.stations.remove(station_id)
            flag_is_middle = False

        if flag_is_middle:
            del station_to_remove.next_stations[self.metroline_id]
            del station_to_remove.previous_stations[self.metroline_id]
            self.stations.remove(station_id)


if __name__ == '__main__':
    map = Map()
    print(1)
    print()
