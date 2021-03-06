import random


def set_random_form(dform: dict, cumul_proba_form: list) -> str:
    """
    :param dform: a dictionary denoting forms and their probabilities of showing up
    :param cumul_proba_form: cumsum of the list of probabilities
    :return: the random form
    """
    rand = random.random()
    index = 0
    while rand > cumul_proba_form[index]:
        index += 1
    return list(dform)[index]
