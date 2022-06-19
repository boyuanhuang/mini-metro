import numpy as np

# Map parameters
MAP_LEVEL = {1: (200, 300), 2: (300, 400), 3: (500, 700), 4: (700, 900)}

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
