import numpy as np
from shapely.geometry import Polygon

# Map parameters
MAP_LEVEL = {1: (300, 200), 2: (400, 300), 3: (700, 500), 4: (900, 700)}
outer = Polygon(((0, 100), (600, 100), (700, 500), (900, 500), (900, 550), (300, 550), (100, 150), (0, 150), (0, 100)))
island = Polygon(((250, 150), (450, 150), (650, 500), (450, 500), (250, 150)))

# Passenger parameters
PASSENGER_FORMS = {'circle': 0.6, 'triangle': 0.2, 'square': 0.2}

# Train parameters
TRAIN_CARRIAGE_CAPACITY = 6
TRAIN_SPEED = 10

# Station parameters
STATION_FORMS = {'circle': 0.6, 'triangle': 0.2, 'square': 0.2}
STATION_CAPACITY = {'Normal': 20, 'Interchange': 30}

# Imputed constant
CUMUL_PROBA_PASSENGER_FORMS = np.cumsum(list(PASSENGER_FORMS.values()))
CUMUL_PROBA_STATION_FORMS = np.cumsum(list(STATION_FORMS.values()))



# Polygon exterior:
polygone_exterior = [(0, 100), (600, 100), (700, 500), (900, 500), (900, 550), (300, 550), (150, 150), (0, 150), (0, 100)]
island = [(250, 150), (450, 150), (650, 500), (450, 500), (250, 150)]

# Define interior "holes":
interiors = {}
interiors[0] = island
i_p = {k: Polygon(v) for k, v in interiors.items()}


WATERZONE = Polygon(polygone_exterior, [zone.exterior.coords for zone in i_p.values() \
                                        if zone.within(Polygon(polygone_exterior)) is True])
