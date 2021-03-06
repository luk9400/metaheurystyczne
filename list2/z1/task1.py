#!/usr/bin/python
""" Finding global minimum of Salomon function"""

from math import cos, pi, sqrt, exp
from time import time
from random import random, gauss


def salomon(x):
    """x is R^4 vector"""

    root_sum = sqrt(sum(i ** 2 for i in x))
    return 1 - cos(2 * pi * root_sum) + 0.1 * root_sum


def tweak(x):
    return [i * gauss(1, 0.1) for i in x]


def decrease(t):
    return t * 0.99


def simulated_annealing(t, x):
    temp = 10 ** 20

    s = x
    best = s

    start = time()
    while time() - start < t and temp > 0:
        r = tweak(s)
        if salomon(r) < salomon(s) or random() < exp((salomon(s) - salomon(r)) / temp):
            s = r
        temp = decrease(temp)
        if salomon(s) <= salomon(best):
            best = s
    return best


if __name__ == "__main__":
    t, x1, x2, x3, x4 = map(int, input().split())
    res = simulated_annealing(t, [x1, x2, x3, x4])
    print(*res, salomon(res))
