from math import exp


def sigmoid(a):
    """
    Checks for over or under flow.
    """
    # Make a equal to limit.
    if (a < -30.0):
        a = -30.00
    elif (a > 30.0):
        a = 30.0
    e = exp(-a)

    return 1 / (1 + e)


def sigmoid_derivative(a):
    """
    Check for over or under flow (derivative).
    """
    if (a < -30.0):
        a = -30.0
    elif (a > 30.0):
        a = 30.0
    e = exp(-a)

    return e / (1 + e)(1 + e)