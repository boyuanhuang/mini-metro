
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

    def link(self, station_list):
        """

        :param station_list:
        :return: True if the linkage is possible,
                 False, if not.
                 Linkage can fail because:
                    1: station-to-link is already present on the metroline
        """
        if len(station_list) < 2:
            return False, 'Please give station_list with at least 2 stations'

        station_issuer, station_to_link = station_list.pop(0), station_list.pop(0)
        is_linkage_finished = (len(station_list) == 0)

        if not self.is_used:
            self.__link_first_2_stations(station_issuer, station_to_link)
            if not is_linkage_finished:
                return self.link([station_to_link] + station_list)
            return True

        if self.metroline_id in station_to_link.attached_metrolines:
            return False, station_to_link

        if station_issuer == self.head_station:
            self.__extend_head_to(station_to_link)
            if not is_linkage_finished:
                return self.link([station_to_link] + station_list)
            return True

        if station_issuer == self.end_station:
            self.__extend_end_to(station_to_link)
            if not is_linkage_finished:
                return self.link([station_to_link] + station_list)
            return True

        # If the station_issuer is a middle station
        station_absorber = station_issuer.next_stations[self.metroline_id]

        station_issuer.next_stations[self.metroline_id] = station_to_link
        station_to_link.next_stations[self.metroline_id] = station_absorber

        station_to_link.previous_stations[self.metroline_id] = station_issuer
        station_absorber.previous_stations[self.metroline_id] = station_to_link
        if not is_linkage_finished:
            return self.link([station_to_link] + station_list)
        return True

    def add_train(self, train, station):
        train.allocate_to_metroline(self, station)
        self.trains.append(train)
        return True

    # region Stations linkage (private methode)
    def __link_first_2_stations(self, station1, station2):
        assert not self.is_used, 'Check not self.is_used condition'
        self.head_station = station1
        self.end_station = station2
        self.stations = [station1, station2]
        self.is_used = True

        # Change stations' properties
        station1.next_stations[self.metroline_id] = station2
        station1.attached_metrolines.append(self.metroline_id)

        station2.previous_stations[self.metroline_id] = station1
        station2.attached_metrolines.append(self.metroline_id)

    def __extend_head_to(self, station):
        if self.is_circular:
            return False
        # Update connected Station's properties :
        old_head_station = self.head_station
        station.next_stations[self.metroline_id] = old_head_station
        old_head_station.previous_stations[self.metroline_id] = station
        station.attached_metrolines.append(self.metroline_id)

        # Update stations list
        self.stations = [station] + self.stations
        self.head_station = station

        # Update metroline properties
        self.is_used = True
        if self.head_station == self.end_station:
            self.is_circular = True

    def __extend_end_to(self, station):
        # Update connected Station's properties :
        old_end_station = self.end_station
        station.previous_stations[self.metroline_id] = old_end_station
        old_end_station.next_stations[self.metroline_id] = station
        station.attached_metrolines.append(self.metroline_id)

        # Update stations list
        self.stations = self.stations + [station]
        self.end_station = station

        self.is_used = True
        if self.head_station == self.end_station:
            self.is_circular = True

    def __remove_station(self, station):
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

        # Update station's properties :
        station.attached_metrolines.remove(self.metroline_id)

        return True
    # endregion


if __name__ == '__main__':
    print('')
