
import config
from engine.util_functions import set_random_form
from engine.passenger import Passenger

class Station():

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
        self.next_stations = dict()  # {metroline_id: Station_id}

        # A station may have several previous-stations connected by different metrolines
        self.previous_stations = dict()  # {metroline_id: Station_id}

    def create_passenger(self):
        self.passengers.append(Passenger())

    def onboard_passenger(self):
        return self.passengers.pop(0)

    def change_station_type(self, type_):
        self.type = type_
        self.capacity = config.STATION_CAPACITY[self.type]

# todo deprecated class, to be deleted
if __name__ == '__main__':
    print(1)
    print()
