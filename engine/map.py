import random
import time

import numpy as np
from shapely.geometry import Point

import config
from engine.util_functions import floyd_warshall
from metroline import MetroLine
from station import Station
from train import Train


def need_update_path_for_passengers(method):
    def update_path_for_passengers_afterward(*args, **kwargs):
        self = args[0]
        method(self, *args[1:], **kwargs)
        self.update_path_for_passengers()

    return update_path_for_passengers_afterward


def need_update_connexion_matrix(method):
    def update_connexion_matrix_afterward(*args, **kwargs):
        self = args[0]
        method(self, *args[1:], **kwargs)
        self.update_connexion_matrix()

    return update_connexion_matrix_afterward


class Map:

    @need_update_connexion_matrix
    def __init__(self):
        # Display

        self.map_level = 1

        # Set waterzone
        self.waterzone = config.WATERZONE

        # Timer and counter
        self.hour = 0
        self.week = 0
        self.day = 0
        self.passenger_transported = 0
        self.number_of_weeks = 1

        # Stations
        self.stations: dict = {}  # {station_id: Station}
        self.station_amount = 0
        while self.station_amount < config.INITIAL_STATION_AMOUNT:
            three_default_forms = ['circle', 'triangle', 'square']
            self.generate_station(form=three_default_forms[self.station_amount])

        # Metrolines
        self.metrolines: dict = {}  # {metroline_id: Metroline}
        self.metroline_amount = 0
        while self.metroline_amount < config.INITIAL_METROLINE_AMOUNT:
            self.receive_new_metroline()

        # Trains
        self.trains = dict()  # {train_id: Train}
        self.train_amount = 0
        while self.train_amount < config.INITIAL_TRAIN_AMOUNT:
            self.receive_new_train()

        # Passengers
        self.passengers = []

        # Carriages
        self.carriage_amount = config.INITIAL_CARRIAGE_AMOUNT

        # Tunnels
        self.tunnel_amount = config.INITIAL_TUNNEL_AMOUNT

        # Distance matrix
        self.distance_matrix = None
        self.transit_matrix = None
        # self.update_connexion_matrix()

        # Widgets # todo

    # region Game interface display
    def display(self):
        pass

    # endregion

    # region Methods for map
    def zoom_out(self):
        self.map_level += 1

    def refresh(self):
        self.update_time_keeper()
        # Generate new station on Wednesday and Saturday
        if (self.hour % config.NRefresh_in_a_week) in [(i + 1) * config.NRefresh_in_a_week // 3 for i in
                                                       range(config.Nnew_stations_per_week)]:
            # self.generate_station()
            pass

        self.generate_passengers()

        if self.is_game_over():
            return False

        self.update_trains()
        return True

    def update_time_keeper(self):
        self.hour += 1
        self.week = self.hour // config.NRefresh_in_a_week
        self.day = (self.hour - self.week * config.NRefresh_in_a_week)//config.Refresh_frequence_per_day
        self.day = config.Week_day[self.day]

    def random_position(self):
        max_x, max_y = config.MAP_LEVEL[self.map_level]
        position = (random.uniform(0, max_x), random.uniform(0, max_y))
        position_point = Point(position)
        while self.waterzone.contains(position_point):
            position = (random.uniform(0, max_x), random.uniform(0, max_y))
            position_point = Point(position)
        return position

    @need_update_path_for_passengers
    def update_connexion_matrix(self):
        """This method should to be called after any routing network modification
        (use need_update_connexion_matrix decorator) """
        # Initialize distance matrix
        distance_matrix = np.array([[np.inf for _ in range(self.station_amount)] for _ in range(self.station_amount)])
        transit_matrix = np.array([[None for _ in range(self.station_amount)] for _ in range(self.station_amount)])
        # for i in range(self.station_amount): # I need diagonal to be inf
        #     distance_matrix[i][i] = 0

        for station_id_ in self.stations.keys():
            current_station = self.get_station(station_id_)
            stations_one_edge_way = list(current_station.next_stations.values()) + \
                                    list(current_station.previous_stations.values())
            while stations_one_edge_way:
                station_one_edge_way = stations_one_edge_way.pop()
                transit_array = [station_id_, station_one_edge_way.station_id]

                distance_matrix[station_id_][station_one_edge_way.station_id] = 1
                transit_matrix[station_id_][station_one_edge_way.station_id] = transit_array

        # Perform Floyd Warshall Algorithm
        self.distance_matrix, self.transit_matrix = floyd_warshall(distance_matrix_to_update=distance_matrix,
                                                                   transit_matrix_to_update=transit_matrix)

        # self.update_path_for_passengers()

    # endregion

    # region Methods for metrolines
    @need_update_connexion_matrix
    def link_metroline_to_stations(self, metroline_id, station_id_list):
        metroline = self.get_metroline(metroline_id)
        station_list = [self.get_station(id_) for id_ in station_id_list]

        # Should we add default train ?
        add_default_train = False
        if (not metroline.is_used) and (not all([train_.is_used for train_ in self.trains.values()])):
            add_default_train = True

        # Build metroline
        metroline.link(station_list)

        # Add default train if needed
        if add_default_train:
            for train_ in self.trains.values():
                if not train_.is_used:
                    metroline.add_train(train_, metroline.head_station)
                    break

        # self.update_connexion_matrix() # decorator used

    def get_metroline(self, id_):
        return self.metrolines[id_]

    # endregion

    # region Methods for stations
    @need_update_connexion_matrix
    def generate_station(self, form=None):
        self.stations[self.station_amount] = Station(station_id=self.station_amount, position=self.random_position(),
                                                     form=form)
        self.station_amount += 1

    @need_update_path_for_passengers
    def generate_passengers(self):
        """ Return False if a station is not able to hold more passengers, else return True"""
        seed = self.hour % config.Refresh_frequence_per_day  # get a number ranged from 0 to 23
        which_week = self.hour // config.NRefresh_in_a_week
        for station_ in self.stations.values():
            draw_a_number = random.randint(0, config.Refresh_frequence_per_day - 1)
            if abs(draw_a_number - seed) <= which_week:
                self.passengers.append(station_.create_passenger())
            if station_.is_gameover():
                return False
        return True

    def get_station(self, id_):
        return self.stations[id_]

    # endregion

    # region Methods for passengers

    def update_path_for_passengers(self):
        """ This method should be called if
         - connexion matrix is updated
         - new passengers generated
         (use need_update_path_for_passengers decorator)
         """
        for station_ in self.stations.values():
            for passenger in station_.passengers:
                feasible_stations = [s_.station_id for s_ in self.stations.values() if s_.form == passenger.form]
                transit_path = np.take(self.transit_matrix[station_.station_id], feasible_stations)
                distance_path = np.take(self.distance_matrix[station_.station_id], feasible_stations)
                if len(transit_path) != 0 and transit_path[0] is not None:  # certain passenger has no path solution
                    passenger.update_path(transit_path=transit_path[np.argmin(distance_path)])
        return True

    # endregion

    # region Methods for trains
    def update_trains(self):
        for train_ in self.trains.values():
            if train_.is_used:
                self.passenger_transported += train_.update()

    def add_train(self, metroline):
        pass

    # endregion

    # region New week arrive :
    def receive_new_train(self):
        self.trains[self.train_amount] = Train(self.train_amount)
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
    def is_game_over(self):
        for station_ in self.stations.values():
            if station_.is_gameover():
                return True
        return False



if __name__ == '__main__':
    if config.Status == 'dev':
        random.seed(0)

    s = time.time()
    citymap = Map()
    citymap.link_metroline_to_stations(metroline_id=0, station_id_list=[0, 1])
    citymap.link_metroline_to_stations(metroline_id=1, station_id_list=[0, 2])
    # citymap.link_metroline_to_stations(metroline_id=2, station_id_list=[0, 1, 2, 3, 4, 5])

    while citymap.hour < 2 * config.NRefresh_in_a_week:
        if citymap.hour == 135:
            print()
        print('H:D:W = ', (citymap.hour, citymap.day, citymap.week), ', nb_passenger_transported = ', citymap.passenger_transported)
        citymap.refresh()
        for station in citymap.stations.values():
            print('Station_', station.station_id, 'Form:', station.form, 'passenger:', station.get_passenger_form())
        print('------')
        for train in citymap.trains.values():
            if train.is_used:
                from_to = str(train.station_about_to_leave.station_id) + '->' + str(train.station_to_visit.station_id)
            else:
                from_to = 'Not used'
            print('Train_', train.train_id,
                  'time_remain:', train.time_remain_to_next_station,
                  'from->to: ', from_to,
                  'passengers:', train.get_passenger_form())

        print('')
        print('')

    # citymap.link_metroline_to_stations(metroline_id=2, station_id_list=[0, 1, 2])
    print(time.time() - s)
    print()
