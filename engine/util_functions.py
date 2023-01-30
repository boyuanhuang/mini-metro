import random
import numpy as np
import config
from shapely.geometry import Point


def set_random_form(dform: dict, except_form: str = None) -> str:
    """
    :param except_form:
    :param dform: a dictionary denoting forms and their probabilities of showing up
    :param cumul_proba_form: cumsum of the list of probabilities
    :return: the random form
    """
    allowed_form = dform.copy()
    if except_form:
        allowed_form.pop(except_form)
    cumul_proba_form = np.cumsum(list(allowed_form.values()))
    rand = random.uniform(0, cumul_proba_form[-1])
    index = 0
    while rand > cumul_proba_form[index]:
        index += 1
    return list(allowed_form)[index]


def floyd_warshall(distance_matrix_to_update, transit_matrix_to_update):
    distance = list(map(lambda i: list(map(lambda j: j, i)), distance_matrix_to_update))
    nVertices = len(distance)
    # Adding vertices individually
    for k in range(nVertices):
        for i in range(nVertices):
            for j in range(nVertices):
                if distance[i][j] > distance[i][k] + distance[k][j]:
                    distance[i][j] = distance[i][k] + distance[k][j]
                    transit_matrix_to_update[i][j] = transit_matrix_to_update[i][k][:-1] + transit_matrix_to_update[k][
                        j]

    return distance, transit_matrix_to_update
