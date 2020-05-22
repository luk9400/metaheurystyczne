""" Algorytm genetyczny do znajdowania minimum funkcji X.S. Yang """

from time import time
from copy import deepcopy
from random import gauss, choice, random
from math import log


def yang(x, epsilon):
    """ x and epsilon are R^5 vectors, x[i] <= 5 (?) """
    return sum([epsilon[i] * abs(x[i]) ** (i + 1) for i in range(len(x))])


def tournament(population, eps):
    P = population
    t = 4

    best = choice(P)
    for _ in range(2, t):
        nxt = choice(P)
        if yang(nxt, eps) < yang(best, eps):
            best = nxt
    return best


def crossover(a, b):
    """ uniform crossover """
    p = 1 / len(a)

    for i in range(len(a)):
        if p >= random():
            a[i], b[i] = b[i], a[i]
    return a, b


def mutate(x):
    return [i * gauss(1, 0.1) for i in x]


def genetic_algorithm(t, x, eps):
    popsize = 10

    P = []
    for _ in range(popsize):
        P.append(mutate(x))

    best = None
    start = time()
    while time() - start < t:
        for p in P:
            if best == None or yang(p, eps) < yang(best, eps):
                best = p
                last_best = time()

        Q = []
        for _ in range(popsize // 2):
            p_a = tournament(deepcopy(P), eps)
            p_b = tournament(deepcopy(P), eps)
            while p_a == p_b:
                p_b = tournament(deepcopy(P), eps)
            c_a, c_b = crossover(deepcopy(p_a), deepcopy(p_b))
            Q.append(mutate(c_a))
            Q.append(mutate(c_b))
        P = Q

        if time() - last_best > log(t):
            break

    return best


def main():
    t, x1, x2, x3, x4, x5, e1, e2, e3, e4, e5 = map(float, input().split())
    result = genetic_algorithm(t, [x1, x2, x3, x4, x5], [e1, e2, e3, e4, e5])
    print(*result, yang(result, [e1, e2, e3, e4, e5]))


if __name__ == "__main__":
    main()
