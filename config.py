import numpy as np

PASSENGER_FORMS = {'circle': 0.6, 'triangle': 0.2, 'square': 0.2}
STATION_FORMS = {'circle': 0.6, 'triangle': 0.2, 'square': 0.2}
TRAIN_WAGON_CAPACITY = 6

### Imputed constant
CUMUL_PROBA_PASSENGER_FORMS = np.cumsum(list(PASSENGER_FORMS.values()))
CUMUL_PROBA_STATION_FORMS = np.cumsum(list(STATION_FORMS.values()))
