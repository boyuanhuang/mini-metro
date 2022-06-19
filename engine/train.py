from config import TRAIN_WAGON_CAPACITY


class Train:

    def __init__(self):
        self.wagon_amount = 1
        self.capacity = TRAIN_WAGON_CAPACITY

        self.passengers = []

    def add_wagon(self):
        self.wagon_amount += 1
        self.capacity += TRAIN_WAGON_CAPACITY

    def load_passenger(self, passenger):
        self.passengers.append(passenger)

    def drop_passenger(self):
        pass