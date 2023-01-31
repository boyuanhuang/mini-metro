import numpy as np
from shapely.geometry import Polygon

# Map parameters
MAP_LEVEL = {1: (300, 200), 2: (400, 300), 3: (700, 500), 4: (900, 700)}
outer = Polygon(((0, 100), (600, 100), (700, 500), (900, 500), (900, 550), (300, 550), (100, 150), (0, 150), (0, 100)))
island = Polygon(((250, 150), (450, 150), (650, 500), (450, 500), (250, 150)))

Refresh_frequence_per_day = 24  # 24 times per second
Nnew_stations_per_week = 2
NRefresh_in_a_week = 7 * Refresh_frequence_per_day

## Widget
INITIAL_TUNNEL_AMOUNT = 2
INITIAL_METROLINE_AMOUNT = 3
INITIAL_TRAIN_AMOUNT = 3
INITIAL_CARRIAGE_AMOUNT = 0

## Passenger parameters
# Passenger form probabilities
PASSENGER_FORMS = {'circle': 0.6, 'triangle': 0.2, 'square': 0.2}

# Train parameters
CARRIAGE_CARRIAGE_CAPACITY = 6
TRAIN_SPEED = 2  # It takes '2' time_unit to travel between stations # todo varibiliser ceci

# Station parameters
INITIAL_STATION_AMOUNT = 3
STATION_FORMS = {'circle': 0.6, 'triangle': 0.2, 'square': 0.2}
STATION_CAPACITY = {'Normal': 20, 'Interchange': 30}

# Imputed constant


# Polygon exterior:
polygone_exterior = [(0, 100), (600, 100), (700, 500), (900, 500), (900, 550), (300, 550), (150, 150), (0, 150),
                     (0, 100)]
island = [(250, 150), (450, 150), (650, 500), (450, 500), (250, 150)]

# Define interior "holes":
interiors = {}
interiors[0] = island
i_p = {k: Polygon(v) for k, v in interiors.items()}

WATERZONE = Polygon(polygone_exterior, [zone.exterior.coords for zone in i_p.values() \
                                        if zone.within(Polygon(polygone_exterior)) is True])
