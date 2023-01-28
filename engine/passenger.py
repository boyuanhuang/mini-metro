import config
from util_functions import set_random_form


class Passenger:

    def __init__(self):
        self.form = set_random_form(config.PASSENGER_FORMS)


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
