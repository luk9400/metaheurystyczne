#!/usr/bin/python
""" Travelling salesman problem with tabu search """


from collections import deque
from time import time


def random_candidate():
    pass


def tweak(s):
    pass


def tabu_search(quality, t):
    l = 100
    n = 10

    s = random_candidate()
    best = s
    L = deque()
    L.append(s)

    start = time()
    while time() - start < t:
        if len(L) > l:
            L.popleft()
        r = tweak(s)

        for i in range(n - 1):
            w = tweak(s)
            if w not in L and (quality(w) < quality(r) or r in L):
                r = w
        if r not in L:
            s = r
            L.append(r)
        if quality(s) < quality(best):
            best = s
    return best


if __name__ == '__main__':
    t, n = map(int, input().split())

    costs = []
    for i in range(n):
        costs.append(list(map(int, input().split())))
    
    print(costs)
