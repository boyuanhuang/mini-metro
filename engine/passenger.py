import config
from util_functions import set_random_form


class Passenger:

    def __init__(self, station, transit_path):
        self.form = set_random_form(config.PASSENGER_FORMS, except_form=station.form)
        self.transit_path = transit_path
        self.initial_station_id = transit_path[0]
        self.current_station_id = transit_path[0]
        self.next_station_id_to_go = transit_path[1]
        self.destination_station_id = transit_path[-1]
        self.is_on_the_train = False

    def update_path(self, transit_path):
        self.transit_path = transit_path
        self.next_station_id_to_go = transit_path[transit_path.index(self.current_station_id)+1]


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
