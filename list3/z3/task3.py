#!usr/bin/python

from time import time
from math import log
from copy import deepcopy
from sys import stderr
from random import randrange, random, choice


directions = {
    "U": (-1, 0),
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
}


def find_position(n, m, grid):
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 5:
                return i, j


def mutate(s):
    i = randrange(len(s))
    j = randrange(len(s))
    s[i], s[j] = s[j], s[i]
    return s


def tournament(population, x, y, grid):
    P = population
    t = 4

    best = choice(P)
    for _ in range(2, t):
        nxt = choice(P)
        if fitness(nxt, x, y, grid) < fitness(best, x, y, grid):
            best = nxt
    return best


def crossover(a, b):
    """ uniform crossover """
    p = 1 / len(a)

    for idx, (_, _) in enumerate(zip(a, b)):
        if p >= random():
            a[idx], b[idx] = b[idx], a[idx]
    return a, b


def fitness(s, x, y, grid):
    i = 0

    for direction in s:
        i += 1
        new_x = x
        new_y = y
        if direction == "U":
            new_x -= 1
        if direction == "R":
            new_y += 1
        if direction == "D":
            new_x += 1
        if direction == "L":
            new_y -= 1

        if grid[new_x][new_y] == 8:
            return i
        if grid[new_x][new_y] != 1:
            x, y = new_x, new_y

    return len(s)


def genetic_algorithm(t, n, m, initial_candidates, popsize, grid):
    x, y = find_position(n, m, grid)

    P = initial_candidates

    best = None
    start = time()
    while time() - start < t:
        for p in P:
            fitness_p = fitness(p, x, y, grid)
            if best == None or fitness_p < fitness(best, x, y, grid):
                best = p[:fitness_p]
                last_best = time()

        Q = []
        for _ in range(popsize // 2):
            p_a = tournament(deepcopy(P), x, y, grid)
            p_b = tournament(deepcopy(P), x, y, grid)
            c_a, c_b = crossover(deepcopy(p_a), deepcopy(p_b))
            Q.append(mutate(c_a))
            Q.append(mutate(c_b))
        P = Q

        if time() - last_best > log(t):
            break

    return best, fitness(best, x, y, grid)


if __name__ == "__main__":
    t, n, m, s, p = map(int, input().split())

    grid = []
    for i in range(n):
        grid.append(list(map(int, list(input())[:m])))

    initial_candidates = []
    for i in range(s):
        initial_candidates.append(list(input()))

    result, qual = genetic_algorithm(t, n, m, initial_candidates, p, grid)
    print(qual)
    print("".join(result), file=stderr)
