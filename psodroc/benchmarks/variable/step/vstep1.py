import vstep


def function(xs):
    return vstep(xs, 1.)


def min(d):
    return vstep.min(d)


def max(d):
    return vstep.max(d)


def is_dimensionality_valid(D):
    return vstep.is_dimensionality_valid(D)
