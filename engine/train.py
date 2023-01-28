from config import CARRIAGE_CARRIAGE_CAPACITY, TRAIN_SPEED


class Train:

    def __init__(self):
        self.carriage_amount = 1
        self.capacity = CARRIAGE_CARRIAGE_CAPACITY
        self.passengers = []
        self.passenger_amount = 0
        self.speed = TRAIN_SPEED

    def add_carriage(self):
        self.carriage_amount += 1
        self.capacity += CARRIAGE_CARRIAGE_CAPACITY

    def load_passenger(self, passenger):
        self.passengers.append(passenger)
        self.passenger_amount += 1

    def drop_passenger(self, station):
        nb_passenger_dropped = 0
        passenger_stayed_onboard = []
        for passenger in self.passengers:
            if passenger.form == station.form:
                nb_passenger_dropped += 1
            else:
                passenger_stayed_onboard.append(passenger)
        self.passengers = passenger_stayed_onboard
        self.passenger_amount -= nb_passenger_dropped
