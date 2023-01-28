

class MetroLine():

    def __init__(self, metroline_id):
        self.metroline_id = metroline_id
        self.head_station_id: int = -1
        self.end_station_id: int = -1
        self.is_circular = (self.head_station_id == self.end_station_id)  # may be not useful ??

        self.stations = []  # [stations_id_1, stations_id_2, ...]

        # Trains on this Metroline
        self.trains = []  # [Train1, Train2, ...]

    def extend_head_to(self, station_id):
        # Update connected Station's properties :
        connected_station = self.get_station(station_id)
        connected_station.next_stations[self.metroline_id] = self.stations[0]
        # Update stations list
        self.stations = [station_id] + self.stations

    def extend_end_to(self, station_id):
        # Update connected Station's properties :
        connected_station = self.get_station(station_id)
        connected_station.previous_stations[self.metroline_id] = self.stations[-1]
        # Update stations list
        self.stations = self.stations + [station_id]

    def remove_station(self, station_id):
        # Update connected Station's properties :
        station_to_remove = self.get_station(station_id)

        flag_is_middle = True

        if station_id == self.head_station_id:
            del station_to_remove.next_stations[self.metroline_id]
            self.stations.remove(station_id)
            flag_is_middle = False

        if station_id == self.end_station_id:
            del station_to_remove.previous_stations[self.metroline_id]
            self.stations.remove(station_id)
            flag_is_middle = False

        if flag_is_middle:
            del station_to_remove.next_stations[self.metroline_id]
            del station_to_remove.previous_stations[self.metroline_id]
            self.stations.remove(station_id)


if __name__ == '__main__':
    print('')
