
class MetroLine:

    def __init__(self, metroline_id):
        self.metroline_id = metroline_id
        self.is_used = False
        self.is_circular = False
        self.head_station = None
        self.end_station = None

        self.stations = []  # [stations_id_1, stations_id_2, ...]

        # Trains on this Metroline
        self.trains = []  # [Train1, Train2, ...]

    def use_new_line(self, station_list):
        assert len(station_list) >= 2, 'Please give station_list with at least 2 stations'
        self.link_first_2_stations(station_list.pop(0), station_list.pop(0))

        while station_list:
            self.extend_end_to(station_list.pop(0))

    def link_first_2_stations(self, station1, station2):
        if not self.is_used:
            self.head_station = station1
            self.end_station = station2
            self.stations = [station1, station2]
            self.is_used = True

            # link Stations level
            station1.next_stations[self.metroline_id] = station2
            station2.previous_stations[self.metroline_id] = station1

    def extend_head_to(self, station):
        if self.is_circular:
            return False
        # Update connected Station's properties :
        old_head_station = self.stations[0]
        station.next_stations[self.metroline_id] = old_head_station
        old_head_station.previous_station[self.metroline_id] = station

        # Update stations list
        self.stations = [station] + self.stations
        self.head_station = station

        # Update metroline properties
        self.is_used = True
        if self.head_station == self.end_station:
            self.is_circular = True

    def extend_end_to(self, station):
        # Update connected Station's properties :
        old_end_station = self.stations[-1]
        station.previous_stations[self.metroline_id] = old_end_station
        old_end_station.next_stations[self.metroline_id] = station

        # Update stations list
        self.stations = self.stations + [station]
        self.end_station = station

        self.is_used = True
        if self.head_station == self.end_station:
            self.is_circular = True

    def remove_station(self, station):
        # Update connected Station's properties :
        station_id = station.station_id
        flag_is_middle = True

        if station == self.head_station:
            del station.next_stations[self.metroline_id]
            self.stations.remove(station.station_id)
            flag_is_middle = False

        if station == self.end_station:
            del station.previous_stations[self.metroline_id]
            self.stations.remove(station_id)
            flag_is_middle = False

        if flag_is_middle:
            del station.next_stations[self.metroline_id]
            del station.previous_stations[self.metroline_id]
            self.stations.remove(station_id)


if __name__ == '__main__':
    print('')
