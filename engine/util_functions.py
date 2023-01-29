import random
import numpy as np
import config
from shapely.geometry import Point


def set_random_form(dform: dict) -> str:
    """
    :param dform: a dictionary denoting forms and their probabilities of showing up
    :param cumul_proba_form: cumsum of the list of probabilities
    :return: the random form
    """
    rand = random.random()
    index = 0
    cumul_proba_form = np.cumsum(list(dform.values()))
    while rand > cumul_proba_form[index]:
        index += 1
    return list(dform)[index]




def floyd_warshall(distance_matrix_to_update):
    distance = list(map(lambda i: list(map(lambda j: j, i)), distance_matrix_to_update))
    nVertices = len(distance)
    # Adding vertices individually
    for k in range(nVertices):
        for i in range(nVertices):
            for j in range(nVertices):
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
    return distance
