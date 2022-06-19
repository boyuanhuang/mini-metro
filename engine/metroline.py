from engine.station import Station


class MetroLine:

    def __init__(self):
        self.id = None
        self.first_station: Station = None
        self.last_station: Station = None


if __name__ == '__main__':
    metroline = MetroLine()
    print(1)
    print()
