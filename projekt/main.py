#!usr/bin/python

from time import time
from math import exp, log
from sys import stderr
from random import randrange, random, choice, choices, randint


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

    if grid[x][y] == 3:
        direction = choice(["R", "L"])
    elif grid[x][y] == 2:
        direction = choice(["U", "D"])
    else:
        direction = choice(list(directions.keys()))

    while len(path) < n * m / 3:
        if grid[x + directions[direction][0]][y + directions[direction][1]] == 8:
            path.append(direction)
            return path, True
        elif grid[x + directions[direction][0]][y + directions[direction][1]] == 1:
            if grid[x][y] == 3:
                direction = choice(["R", "L"])
            elif grid[x][y] == 2:
                direction = choice(["U", "D"])
            else:
                direction = choice(list(directions.keys()))
        else:
            x += directions[direction][0]
            y += directions[direction][1]
            path.append(direction)
            if random() < 0.15:
                if grid[x][y] == 3:
                    direction = choice(["R", "L"])
                elif grid[x][y] == 2:
                    direction = choice(["U", "D"])
                else:
                    direction = choice(list(directions.keys()))

    return path, False


def initial_candidate(x, y, grid):
    path, is_correct = random_walk(x, y, grid)

    while not is_correct:
        path, is_correct = random_walk(x, y, grid)

    return path


def tweak(s):
    i = randrange(len(s))
    j = randrange(i, len(s))
    if 0.8 > random():
        return s[: i + 1] + s[j:i:-1] + s[j + 1 :]
    else:
        return s[: i + 1] + choices(["U", "R", "D", "L"], k=j - i) + s[j + 1 :]


def quality(s, x, y, grid, maxsize):
    i = 0

    for direction in s:
        i += 1
        new_x = x
        new_y = y

        if direction == "U":
            new_x -= 1
            if grid[new_x][new_y] == 3:
                continue
        if direction == "R":
            new_y += 1
            if grid[new_x][new_y] == 2:
                continue
        if direction == "D":
            new_x += 1
            if grid[new_x][new_y] == 3:
                continue
        if direction == "L":
            new_y -= 1
            if grid[new_x][new_y] == 2:
                continue

        if grid[new_x][new_y] == 8:
            return i
        if grid[new_x][new_y] != 1:
            x, y = new_x, new_y

    return maxsize


def decrease(t):
    return t * 0.9


def simulated_annealing(t, n, m, grid, initial_solution):
    temp = 1000
    maxsize = n * m

    x, y = find_position(n, m, grid)
    _quality = lambda s: quality(s, x, y, grid, maxsize)

    s = initial_candidate(x, y, grid)
    best = s
    last_best = None

    start = time()
    while time() - start < t and temp > 0:
        r = tweak(s)
        quality_r = _quality(r)

        if quality_r < _quality(s) or random() < exp((_quality(s) - quality_r) / temp):
            s = r[:quality_r]

        temp = decrease(temp)

        quality_s = _quality(s)
        if quality_s < _quality(best):
            best = s[:quality_s]
            last_best = time()

        if last_best != None and time() - last_best > min(
            0.5 * log(t), 0.5 * log(n * m / 10)
        ):
            break

    return best, _quality(best)


if __name__ == "__main__":
    t, n, m = map(int, input().split())

    grid = []
    for i in range(n):
        grid.append(list(map(int, list(input())[:m])))

    initial_solution = list(input())

    result, qual = simulated_annealing(t, n, m, grid, initial_solution)
    print(qual)
    print("".join(result), file=stderr)
