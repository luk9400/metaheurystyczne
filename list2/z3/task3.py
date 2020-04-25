#!usr/bin/python

from time import time
from math import exp
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


def random_walk(x, y, grid):
    path = []
    direction = choice(list(directions.keys()))

    while len(path) < n * m / 3:
        if grid[x + directions[direction][0]][y + directions[direction][1]] == 8:
            path.append(direction)
            return path, True
        elif grid[x + directions[direction][0]][y + directions[direction][1]] == 1:
            direction = choice(list(directions.keys()))
        else:
            x += directions[direction][0]
            y += directions[direction][1]
            path.append(direction)
            if random() < 0.15:
                direction = choice(list(directions.keys()))
    return path, False


def initial_candidate(x, y, grid):
    path, is_correct = random_walk(x, y, grid)

    while not is_correct:
        path, is_correct = random_walk(x, y, grid)

    return path


def tweak(s):
    i = randrange(len(s))
    j = randrange(len(s))
    s[i], s[j] = s[j], s[i]
    return s


def quality(s, x, y, grid):
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


def decrease(t):
    return t * 0.99


def simulated_annealing(t, n, m, grid):
    temp = 10 ** 5

    x, y = find_position(n, m, grid)
    s = initial_candidate(x, y, grid)
    print(quality(s, x, y, grid))
    best = s

    start = time()
    while time() - start < t and temp > 0:
        r = tweak(s)
        quality_r = quality(r, x, y, grid)
        if quality_r < quality(s, x, y, grid) or random() < exp(
            (quality(s, x, y, grid) - quality_r) / temp
        ):
            s = r[:quality_r]
        temp = decrease(temp)
        quality_s = quality(s, x, y, grid)
        if quality_s < quality(best, x, y, grid):
            best = s[:quality_s]
    return best, quality(best, x, y, grid)


if __name__ == "__main__":
    t, n, m = map(int, input().split())

    grid = []
    for i in range(n):
        grid.append(list(map(int, list(input())[:m])))

    result, qual = simulated_annealing(t, n, m, grid)
    print(qual)
    print("".join(result), file=stderr)
