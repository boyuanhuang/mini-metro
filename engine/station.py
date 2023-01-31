import math

import config
from engine.util_functions import set_random_form
from engine.passenger import Passenger


class Station:

    def __init__(self, station_id, position):
        self.station_id = station_id
        self.position = position
        self.form = set_random_form(config.STATION_FORMS)
        self.type = 'Normal'
        self.capacity = config.STATION_CAPACITY[self.type]
        self.timer = None
        self.passengers = []
        self.attached_metrolines = []

        # A station may have several next-stations connected by different metrolines
        self.next_stations = dict()  # {metroline_id: Station}

        # A station may have several previous-stations connected by different metrolines
        self.previous_stations = dict()  # {metroline_id: Station}

    def create_passenger(self, transit_matrix):
        new_passenger = Passenger(self, transit_matrix)
        self.passengers.append(new_passenger)
        return new_passenger

    def onboard_passenger(self):
        return self.passengers.pop(0)

    def change_station_type(self, type_):
        self.type = type_
        self.capacity = config.STATION_CAPACITY[self.type]

    def distance_with(self, station2):
        return math.sqrt(
            (self.position[0] - station2.position[0]) ** 2 + (self.position[0] - station2.position[0]) ** 2)

    def get_next_station_for_train(self, metroline):
        if self == metroline.end_station and not metroline.is_circular:
            return self.previous_stations[metroline.metroline_id]
        if metroline.metroline_id in self.next_stations.keys():
            return self.next_stations[metroline.metroline_id]
        return False


# todo deprecated class, to be deleted
if __name__ == '__main__':
    print()
