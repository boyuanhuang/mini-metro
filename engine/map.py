import random

import numpy as np

import config
from station import Station
from metroline import MetroLine
from shapely.geometry import Point


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
        self.timer = None
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
        self.distance_matrix = self.update_distance_matrix()

        # Tool

        # todo

    def display(self):
        pass

    def generate_station(self):
        self.stations[self.station_amount] = Station(station_id=self.station_amount, position=self.random_position())
        self.station_amount += 1

    def zoom_out(self):
        self.map_level += 1

    def random_position(self):
        max_x, max_y = config.MAP_LEVEL[self.map_level]
        position = (random.uniform(0, max_x), random.uniform(0, max_y))
        position_point = Point(position)
        while self.waterzone.contains(position_point):
            position = (random.uniform(0, max_x), random.uniform(0, max_y))
            position_point = Point(position)
        return position

    def get_station(self, id_):
        return self.stations[id_]

    def get_metroline(self, id_):
        return self.metrolines[id_]

    # New week arrive :
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

    def update_distance_matrix(self):
        # Initialize distance matrix
        distance_matrix = [[np.inf for _ in range(self.station_amount)] for _ in range(self.station_amount)]
        for i in range(self.station_amount):
            distance_matrix[i][i] = 0

        for station_id in self.stations.keys():
            current_station = self.get_station(station_id)
            stations_one_edge_way = list(current_station.next_stations.values()) + \
                                    list(current_station.previous_stations.values())
            while stations_one_edge_way:
                station_one_edge_way = stations_one_edge_way.pop()
                distance_matrix[station_id][station_one_edge_way.station_id] = 1

        return distance_matrix

    # Operate metrolines
    def test_attach_metroline_to_station(self, metroline_id, station_id_list):
        metroline = self.get_metroline(metroline_id)
        station_list = [self.get_station(id_) for id_ in station_id_list]
        metroline.use_new_line(station_list)
        self.update_distance_matrix()


if __name__ == '__main__':
    print()
    citymap = Map()
    citymap.test_attach_metroline_to_station(metroline_id=0, station_id_list=[0, 1, 2, 0])
    print(1)
    print()
