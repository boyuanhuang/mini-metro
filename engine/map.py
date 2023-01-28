import random

import numpy as np

import config
from station import Station
from metroline import MetroLine


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

    # New week arrive :
    def receive_new_train(self):
        self.train_amount += 1

    def receive_new_metroline(self):
        self.metrolines.append(MetroLine(len(self.metrolines)) + 1)
        self.metroline_amount += 1

    def receive_new_tunnel(self):
        self.tunnel_amount += 1

    def receive_new_carriage(self):
        self.carriage_amount += 1

    def new_week_arrive(self):
        self.receive_new_train()

        # todo : to be imporved, in the real game, player chooses one among 2 proposed choices
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
        distance_matrix = [[np.inf for _ in range(self.station_amount)]]
        for station_id in self.stations.keys():
            todo

        return distance_matrix


if __name__ == '__main__':
    map = Map()
    print(1)
    print()
