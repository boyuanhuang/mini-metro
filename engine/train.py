import config
from config import CARRIAGE_CARRIAGE_CAPACITY, TRAIN_SPEED


class Train:

    def __init__(self, train_id=None):
        self.train_id = train_id
        self.carriage_amount = 1
        self.capacity = CARRIAGE_CARRIAGE_CAPACITY
        self.passengers = []
        self.passenger_amount = 0
        self.speed = TRAIN_SPEED

        self.is_used = False
        self.metroline = None
        self.is_at_station = True
        self.station_about_to_leave = None
        self.station_to_visit = None
        self.time_remain_to_next_station = None

    def allocate_to_metroline(self, metroline, station):
        self.is_used = True
        self.metroline = metroline
        self.is_at_station = True
        self.station_about_to_leave = station
        self.station_to_visit = station.get_next_station_for_train(metroline)

    def update(self):
        if self.is_at_station:
            self.drop_passenger()
            self.load_passenger()
            self.leave_from_current_station()
        else:
            self.time_remain_to_next_station -= 1
            if self.time_remain_to_next_station == 0:
                self.arrive_to_station()

    # Possible operations for a train
    def add_carriage(self):
        self.carriage_amount += 1
        self.capacity += CARRIAGE_CARRIAGE_CAPACITY

    def remove_carriage(self):
        pass

    def load_passenger(self):
        # todo : how can a passenger decide to go on the train ?
        # todo : update station's passenger list
        """load passengers at station_about_to_leave"""
        for passenger in self.station_about_to_leave.passengers:
            self.passengers.append(passenger)
            self.passenger_amount += 1

    def drop_passenger(self):
        # todo : how can a passenger decide to go down the train ? Transit problem ?
        # todo : update station's passenger list
        # todo update passenger information if transit
        """load passengers at station_about_to_leave"""
        nb_passenger_dropped = 0
        passenger_stayed_onboard = []
        for passenger in self.passengers:
            if passenger.form == self.station_about_to_leave.form:
                nb_passenger_dropped += 1
            else:
                passenger_stayed_onboard.append(passenger)
        self.passengers = passenger_stayed_onboard
        self.passenger_amount -= nb_passenger_dropped

    def arrive_to_station(self):
        self.is_at_station = True
        self.station_about_to_leave = self.station_to_visit
        self.station_to_visit = self.station_about_to_leave.get_next_station_for_train(self.metroline)

    def leave_from_current_station(self):
        self.is_at_station = False
        self.time_remain_to_next_station = self.__compute_commute_time()

    def __compute_commute_time(self):
        return self.station_about_to_leave.distance_with(self.station_to_visit) // config.TRAIN_SPEED
