#!/usr/bin/python
""" Travelling salesman problem with tabu search """


from collections import deque
from time import time
from itertools import permutations
from math import factorial
import random
import math
import sys


def random_candidate(n):
    perm = []
    while len(perm) < n - 1:
        rand = random.randrange(1, n)
        if rand not in perm:
            perm.append(rand)
    return [0] + perm + [0]


def greedy_candidate(n, costs):
    path = [0]
    current_city = 0
    while len(path) < n:
        min_cost = math.inf
        min_index = 0

        for i, _ in enumerate(costs[current_city]):
            if costs[current_city][i] < min_cost and i not in path:
                min_cost = costs[current_city][i]
                min_index = i
        path.append(min_index)
        current_city = min_index
    return path + [0]


def tweak(s):
    i = random.randrange(1, len(s) - 2)
    j = random.randrange(1, len(s) - 2)
    s[i], s[j] = s[j], s[i]
    return s


def quality(s, costs):
    acc = 0
    for i in range(len(s) - 1):
        acc += costs[s[i]][s[i + 1]]
    return acc


def tabu_search(t, size, costs):
    l = 1000
    n = 10000

    s = greedy_candidate(size, costs)
    best = s
    L = deque()
    L.append(s)

    start = time()
    while time() - start < t:
        if len(L) > l:
            L.popleft()
        r = tweak(s)

        for _ in range(n - 1):
            w = tweak(s)
            if w not in L and (quality(w, costs) < quality(r, costs) or r in L):
                r = w
        if r not in L:
            s = r
            L.append(r)
        if quality(s, costs) < quality(best, costs):
            best = s
    return best


if __name__ == '__main__':
    t, n = map(int, input().split())

    costs = []
    for i in range(n):
        costs.append(list(map(int, input().split())))

    result = tabu_search(t, n, costs)
    print(quality(result, costs))
    print(*list(map(lambda i: i + 1, result)), file=sys.stderr)
