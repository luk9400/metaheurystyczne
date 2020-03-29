#!usr/bin/python
""" Some problem with tabu search """


from collections import deque
from time import time
import random


directions = {
    'U': (-1, 0),
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
}


def find_position(n, m, grid):
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 5:
                return i, j


def exit_nearby(x, y, grid):
    if grid[x - 1][y] == 8:
        return 'U'
    elif grid[x][y + 1] == 8:
        return 'R'
    elif grid[x + 1][y] == 8:
        return 'D'
    elif grid[x][y - 1] == 8:
        return 'L'
    else:
        return None


def initial_candidate(x, y, grid):
    path = []

    dirs = list(directions.values())
    dirs_lit = list(directions)
    current_dir = 0
    while grid[x][y] != 8:
        exit = exit_nearby(x, y, grid)
        if exit:
            path.append(exit)
            break

        dir_x, dir_y = dirs[current_dir]
        new_x = x + dir_x
        new_y = y + dir_y

        if grid[new_x][new_y] == 1:
            current_dir = (current_dir + 1) % 4
        else:
            x, y = new_x, new_y
            path.append(dirs_lit[current_dir])

    return path


def tweak(s):
    i = random.randrange(len(s))
    j = random.randrange(len(s))
    s[i], s[j] = s[j], s[i]
    return s


def quality(s, x, y, grid):
    i = 0

    for direction in s:
        i += 1
        new_x = x
        new_y = y
        if direction == 'U':
            new_x -= 1
        if direction == 'R':
            new_y += 1
        if direction == 'D':
            new_x += 1
        if direction == 'L':
            new_y -= 1

        if grid[new_x][new_y] == 8:
            return i
        if grid[new_x][new_y] != 1:
            x, y = new_x, new_y

    return len(s)


def tabu_search(t, n, m, grid):
    l = 100
    tweaks = n**2

    x, y = find_position(n, m, grid)
    s = initial_candidate(x, y, grid)
    best = s
    L = deque()
    L.append(s)

    start = time()
    while time() - start < t:
        if len(L) > l:
            L.popleft()
        r = tweak(s)

        for _ in range(tweaks - 1):
            w = tweak(s)
            quality_w = quality(w, x, y, grid)
            if w[:quality_w] not in L and (quality_w < quality(r, x, y, grid) or r in L):
                r = w[:quality_w]
        if r not in L:
            s = r
            L.append(r)
        quality_s = quality(s, x, y, grid)
        if quality_s < quality(best, x, y, grid):
            best = s[:quality_s]
    return best, quality(best, x, y, grid)


if __name__ == '__main__':
    t, n, m = map(int, input().split())

    grid = []
    for i in range(n):
        grid.append(list(map(int, list(input())[:m])))

    result, qual = tabu_search(t, n, m, grid)
    print(qual)
    print("".join(result))
