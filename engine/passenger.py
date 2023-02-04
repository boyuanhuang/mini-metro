import config
from util_functions import set_random_form


class Passenger:

    def __init__(self, station, transit_path=None):
        self.form = set_random_form(config.PASSENGER_FORMS, except_form=station.form)
        self.transit_path = transit_path
        self.initial_station_id = station.station_id
        self.current_station_id = station.station_id
        self.next_station_id_to_go = None # todo
        self.destination_station_id = None # todo
        self.is_on_the_train = False
        self.reach_destination = False

    def update_path(self, transit_path=None):
        if transit_path:
            self.transit_path = transit_path
        self.next_station_id_to_go = self.transit_path[self.transit_path.index(self.current_station_id)+1]
        self.destination_station_id = self.transit_path[-1]

    def passenger_arrive_to_station(self, station):
        if self.form == station.form:
            self.reach_destination = True
        self.current_station_id = station.station_id





if __name__ == '__main__':
    import time

    start = time.time()
    forms = {'circle': 0, 'triangle': 0, 'square': 0}

    for i in range(1000):
        p = Passenger()
        forms[p.form] += 1
    print(forms)

    print(time.time() - start)
    # p.set_random_form()
    # d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
    #
    # l = list(d)
    # r = random.choice(l)
    # print()
