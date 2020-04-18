from random import randint, uniform


def integer_generator(a, b):
    """
    Generates a random integer between a and b.
    """
    return randint(abs(int(a)),abs(int(b)))

def float_generator(a,b):
    """
    Generates a random integer between a and b.
    """
    return uniform(a,b)

def check_random_int(r):
    """
    Checks random int and assigns the correct choice.
    """
    if r <= 29:
        choice = 1
    elif r <= 64:
        choice = 2
    else:
        choice = 3
    return choice

