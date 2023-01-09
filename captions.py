# flake8: noqa
from random import choice


def randomize_18(answer):
    """The ratio of the metric in xvalue1 to that in xval2 is answer."""
    equals = [
        "The {{ metric }} in {{ xvalue1 }} is equal to that in {{ xvalue2 }}.",
        "The {{ metric }} in {{ xvalue2 }} is equal to that in {{ xvalue1 }}.",
        "The {{ metric }} in {{ xvalue1 }} is the same as that in {{ xvalue2 }}.",
        "The {{ metric }} in {{ xvalue2 }} is the same as that in {{ xvalue1 }}."
    ]
    greaters = [  # xvalue1 / xvalue2 > 1
        "The {{ metric }} in {{ xvalue1 }} is {{ answer }} times greater than that in {{ xvalue2 }}.",
        "The {{ metric }} in {{ xvalue1 }} is greater than that in {{ xvalue2 }} by a factor of {{ answer }}.",
        "The ratio of the {{ metric }} in {{ xvalue1 }} to that in {{ xvalue2 }} is {{ answer }}.",
        "The ratio of the {{ metric }} in {{ xvalue2 }} to that in {{ xvalue1 }} is {{ 1 / answer }}."
    ]
    lessers = [  # xvalue1 / xvalue2 < 1
        "The {{ metric }} in {{ xvalue2 }} is {{ 1 / answer }} times greater than that in {{ xvalue1 }}.",
        "The {{ metric }} in {{ xvalue2 }} is greater than that in {{ xvalue1 }} by a factor of {{ 1 / answer }}.",
        "The ratio of the {{ metric }} in {{ xvalue1 }} to that in {{ xvalue2 }} is {{ answer }}.",
        "The ratio of the {{ metric }} in {{ xvalue2 }} to that in {{ xvalue1 }} is {{ 1 / answer }}."
    ]
    if answer == 1:
        return choice(equals)
    if answer > 1:
        return choice(greaters)
    return choice(lessers)


def randomize_37(answer):
    """The difference between the metric in x1 and that in x2 is answer."""
    equals = [  # metric == 0
        "There is no difference between the {{ metric }} in {{ xvalue1 }} and that in {{ xvalue2 }}.",
        "There is no difference between the {{ metric }} in {{ xvalue2 }} and that in {{ xvalue1 }}.",
        "The {{ metric }} in {{ xvalue1 }} is equal to that in {{ xvalue2 }}.",
        "The {{ metric }} in {{ xvalue2 }} is equal to that in {{ xvalue1 }}.",
        "The {{ metric }} in {{ xvalue2 }} is the same as that in {{ xvalue1 }}.",
        "The {{ metric }} in {{ xvalue1 }} is the same as that in {{ xvalue2 }}."
    ]
    greaters = [  # metric > 0
        "The {{ metric }} in {{ xvalue1 }} exceeds that in {{ xvalue2 }} by {{ answer }}.",
        "The {{ metric }} in {{ xvalue1 }} is greater than that in {{ xvalue2 }} by {{ answer }}.",
        "The {{ metric }} in {{ xvalue2 }} is less than that in {{ xvalue1 }} by {{ answer }}.",
        "The {{ metric }} in {{ xvalue1 }} is {{ answer }} more than that in {{ xvalue2 }}.",
        "The difference between the {{ metric }} in {{ xvalue1 }} and that in {{ xvalue2 }} is {{ answer }}."
    ]
    lessers = [  # metric < 0
        "The {{ metric }} in {{ xvalue2 }} exceeds that in {{ xvalue1 }} by {{ -1 * answer }}.",
        "The {{ metric }} in {{ xvalue2 }} is greater than that in {{ xvalue1 }} by {{ -1 * answer }}.",
        "The {{ metric }} in {{ xvalue1 }} is less than that in {{ xvalue2 }} by {{ -1 * answer }}.",
        "The {{ metric }} in {{ xvalue2 }} is {{ -1 * answer }} more than that in {{ xvalue1 }}.",
        "The difference between the {{ metric }} in {{ xvalue2 }} and that in {{ xvalue1 }} is {{ -1 * answer }}."
    ]
    if answer == 0:
        return choice(equals)
    if answer > 0:
        return choice(greaters)
    return choice(lessers)


def randomize_39(answer):
    """The difference between X and Y is answer.""",
    greaters = [
        "The {{ X }} is higher than the {{ Y }} by {{ answer }}.",
        "The {{ X }} is greater than the {{ Y }} by {{ answer }}.",
        "The {{ X }} exceeds the {{ Y }} by {{ answer }}.",
        "The {{ Y }} is less than the {{ X }} by {{ answer }}."
    ]
    lessers = [
        "The {{ Y }} is higher than the {{ X }} by {{ answer }}.",
        "The {{ Y }} is greater than the {{ X }} by {{ answer }}.",
        "The {{ Y }} exceeds the {{ X }} by {{ answer }}."
    ]
    unequals = [
        "The difference between the {{ X }} and the {{ Y }} is {{ answer }}.",
        "The {{ X }} and the {{ Y }} differ by {{ answer }}.",
        "The difference between the {{ Y }} and the {{ X }} is {{ answer }}.",
        "The {{ Y }} and the {{ X }} differ by {{ answer }}.",
        "{{ answer }} is the difference between the {{ X }} and the {{ Y }}.",
        "{{ answer }} is the difference between the {{ Y }} and the {{ X }}."
    ]
    equals = [
        "The {{ X }} is equal to the {{ Y }}.",
        "The {{ Y }} is equal to the {{ X }}.",
        "The {{ X }} is the same as the {{ Y }}.",
        "The {{ Y }} is the same as the {{ X }}.",
        "There is no difference between the {{ X }} and the {{ Y }}.",
        "There is no difference between the {{ Y }} and the {{ X }}."
    ]
    if answer == 0:
        return choice(equals)
    if answer > 0:
        choices = choice(unequals, greaters)
        return choice(choices)
    choices = choice(unequals, lessers)
    return choice(choices)


def randomize_42(answer):
    """In the year y, what is the difference between A and B?"""
