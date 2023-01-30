import math
import time

import numpy as np

import random
from shapely.geometry import Point

import config
from engine.util_functions import floyd_warshall

from metroline import MetroLine
from station import Station


class Map:

    def __init__(self):
        # Display
        self.map_level = 1

        # Set waterzone
        self.waterzone = config.WATERZONE

        # Initialize metrolines
        self.metrolines: dict = {}  # {metroline_id: Metroline}

        # Initialize stations
        self.stations: dict = {}  # {station_id: Station}
        self.station_amount = 0
        while self.station_amount < config.INITIAL_STATION_AMOUNT:
            self.generate_station()

        # Timer and counter
        self.timer = 0
        self.passenger_transported = 0
        self.number_of_weeks = 1

        # Widget that we dispose :
        self.metroline_amount = 0
        while self.metroline_amount < config.INITIAL_METROLINE_AMOUNT:
            self.receive_new_metroline()

        self.train_amount = config.INITIAL_TRAIN_AMOUNT
        self.tunnel_amount = config.INITIAL_TUNNEL_AMOUNT
        self.carriage_amount = config.INITIAL_CARRIAGE_AMOUNT

        # Distance matrix
        self.distance_matrix = None
        self.transit_matrix = None
        self.update_connexion_matrix()

        # Widgets # todo

        self.refresh()

    # region Game interface display
    def display(self):
        pass

    # endregion

    # region Methods for map
    def zoom_out(self):
        self.map_level += 1

    def refresh(self):
        self.timer += 1
        # Generate new station on Wednesday and Saturday
        if self.timer % config.NRefresh_in_a_week in [(i + 1) * config.NRefresh_in_a_week // 3 for i in range(config.Nnew_stations_per_week)]:
            self.generate_station()
        self.generate_passengers()

    def random_position(self):
        max_x, max_y = config.MAP_LEVEL[self.map_level]
        position = (random.uniform(0, max_x), random.uniform(0, max_y))
        position_point = Point(position)
        while self.waterzone.contains(position_point):
            position = (random.uniform(0, max_x), random.uniform(0, max_y))
            position_point = Point(position)
        return position

    def update_connexion_matrix(self):
        # Initialize distance matrix
        distance_matrix = np.array([[np.inf for _ in range(self.station_amount)] for _ in range(self.station_amount)])
        # todo : denote transit [[1->2, 1-> 3], [2->1->3, ...]] while updating with Floyd Warshall Algorithm
        transit_matrix = np.array([[None for _ in range(self.station_amount)] for _ in range(self.station_amount)])
        # for i in range(self.station_amount): # I need diagonal to be inf
        #     distance_matrix[i][i] = 0

        for station_id in self.stations.keys():
            current_station = self.get_station(station_id)
            stations_one_edge_way = list(current_station.next_stations.values()) + \
                                    list(current_station.previous_stations.values())
            while stations_one_edge_way:
                station_one_edge_way = stations_one_edge_way.pop()
                transit_array = [station_id, station_one_edge_way.station_id]

                distance_matrix[station_id][station_one_edge_way.station_id] = 1
                transit_matrix[station_id][station_one_edge_way.station_id] = transit_array

        # Perform Floyd Warshall Algorithm
        self.distance_matrix, self.transit_matrix = floyd_warshall(distance_matrix_to_update=distance_matrix,
                                                                   transit_matrix_to_update=transit_matrix)

    # endregion

    # region Methods for metrolines
    def link_metroline_to_stations(self, metroline_id, station_id_list):
        metroline = self.get_metroline(metroline_id)
        station_list = [self.get_station(id_) for id_ in station_id_list]
        metroline.link(station_list)
        self.update_connexion_matrix()

    # endregion

    # region Methods for stations
    def generate_station(self):
        self.stations[self.station_amount] = Station(station_id=self.station_amount, position=self.random_position())
        self.station_amount += 1

    def generate_passengers(self):
        for station in self.stations.values():
            if random.uniform(0, self.timer) > math.sqrt(self.timer): # todo : generating too many pasengers !! to fix bug
                station.create_passenger()

    def get_station(self, id_):
        return self.stations[id_]

    def get_metroline(self, id_):
        return self.metrolines[id_]

    # endregion

    # region Methods for passengers
    def update_passengers_destination(self):
        for station in self.stations:
            for passenger in station.passengers:
                feasible_stations = [s_.station_id for s_ in self.stations if s_.form == passenger.form]
                transit_matrix = np.take(self.transit_matrix[station.station_id], feasible_stations)
                distance_matrix = np.take(self.distance_matrix[station.station_id], feasible_stations)
                passenger.destination_station_id = transit_matrix[np.argmin(distance_matrix)]
        return True

    # endregion

    # region New week arrive :
    def receive_new_train(self):
        self.train_amount += 1

    def receive_new_metroline(self):
        self.metrolines[self.metroline_amount] = MetroLine(self.metroline_amount)
        self.metroline_amount += 1

    def receive_new_tunnel(self):
        self.tunnel_amount += 1

    def receive_new_carriage(self):
        self.carriage_amount += 1

    def new_week_arrive(self):
        self.receive_new_train()

        # todo : to be improved, in the real game, player chooses one among 2 proposed choices
        if self.number_of_weeks % 3 == 0:
            self.receive_new_metroline()
            self.receive_new_tunnel()

        elif self.number_of_weeks % 3 == 1:
            self.receive_new_metroline()
            self.receive_new_carriage()

        else:
            self.receive_new_carriage()
            self.receive_new_tunnel()
    # endregion


if __name__ == '__main__':
    print()
    s = time.time()
    citymap = Map()
    citymap.link_metroline_to_stations(metroline_id=0, station_id_list=[0, 1])
    citymap.link_metroline_to_stations(metroline_id=1, station_id_list=[0, 2])

    while citymap.timer < config.NRefresh_in_a_week:
        citymap.refresh()

    # citymap.link_metroline_to_stations(metroline_id=2, station_id_list=[0, 1, 2])
    print(time.time() - s)
    print(1)
    print()
