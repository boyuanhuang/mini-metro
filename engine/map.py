from engine.metroline import MetroLine
from engine.station import Station


class Map:

    def __init__(self):
        self.metrolines: list[MetroLine] = None
        self.stations: list[Station] = []
        self.station_amount = 0
        self.waterzone = None

    def display(self):
        pass

    def generate_station(self):
        self.station_amount += 1
        self.stations.append(Station(number=self.station_amount))




if __name__ == '__main__':
    map = Map()
    print(1)
    print()