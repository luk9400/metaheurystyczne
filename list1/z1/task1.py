#!/usr/bin/python
""" Finding global minimum of HappyCat and Griewank functions """

import sys
import random
from math import cos
from operator import mul
from functools import reduce
from time import time


def norm(x):
    """ Returns norm of a vector """
    return sum([i**2 for i in x])**(1/2)


def h(x):
    """ HappyCat function. x is a vector. At our case it's R^4 vector.  """
    return ((norm(x)**2 - 4)**2)**(1/8) + (1/4) * ((1/2) * norm(x)**2 + sum(x)) + (1/2)


def g(x):
    """ Griewank function. x is a vector. At our case it's R^4 vector. """
    return 1 + sum([i**2 / 4000 for i in x]) - reduce(mul, [cos(a / (i + 1)**(1/2)) for i, a in enumerate(x)], 1)


def random_vector():
    """ Returns random R^4 vector """
    v = []
    for _ in range(4):
        v.append(random.uniform(-2, 2))
    return v


def tweak(vector):
    v = []
    for i in vector:
        v.append(i + random.gauss(0, 0.01)) 
    return v
        

def hill_climbing(func, t):
    """ hill climbing with random restarts """
    s = random_vector()
    best = s

    start = time()
    while time() - start < t:
        time_interval = t / 1000
        inner_start = time()
        while time() - start < t and time() - inner_start < time_interval:
            r = tweak(s)
            if func(r) < func(s):
                s = r
        if func(s) < func(best):
            best = s
        s = random_vector()
    return best


if __name__ == '__main__':
    if len(sys.argv) == 3:
        t = int(sys.argv[1])
        b = int(sys.argv[2])
        if b == 0:
            result = hill_climbing(h, t)
            print(result, h(result))
        else:
            result = hill_climbing(g, t)
            print(result, g(result))
    else:
        print("main [time in s] [if 0 minimize h(X) else minimize g(x)]")
