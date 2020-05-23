from time import time
from copy import deepcopy
from math import log
from random import gauss, choice, random, randrange, choices, randint
from sys import stderr
from collections import Counter


def mutate(s, multiset, dictionary):
    letters = Counter(s)
    remaining_dict = {char: multiset[char][1] - letters[char] for char in multiset}
    chars = [char for char, value in remaining_dict.items() if value > 0]
    if not chars:
        return s

    p = random()

    if p < 0.2:
        return s + choices(chars, k=randint(1, 2))
    if p < 0.3:
        idx = randrange(0, len(s))
        return s[:idx] + choices(chars, k=randint(1, 2)) + s[idx:]
    if p < 0.5:
        for i in range(len(s)):
            if random() < 0.1:
                s[i] = choice(chars)
        return s
    return s


def tournament(population, multiset, dictionary):
    _fitness = lambda x: fitness(x, deepcopy(multiset), dictionary)
    P = population
    t = 4

    best = choice(P)
    for _ in range(2, t):
        nxt = choice(P)
        if _fitness(nxt) > _fitness(best):
            best = nxt
    return best


def fitness(s, multiset, dictionary):
    value = 0
    if "".join(s) in dictionary:
        for char in s:
            if multiset[char][1] > 0:
                value += multiset[char][0]
                multiset[char] = (multiset[char][0], multiset[char][1] - 1)
            else:
                return 0
        return value
    else:
        return 0


# def crossover(a, b):
#     # idx_a = randrange(0, len(a))
#     # idx_b = randrange(0, len(b))

#     # p_a, p_b = a[:idx_a] + b[idx_b:], a[idx_a:] + b[:idx_b]

#     for i in range(min(len(a), len(b))):
#         if random() < 0.1:
#             a[i], b[i] = b[i], a[i]

#     return a, b

def twoPointCrossover(pa, pb):
    i1a, i2a = choices(range(len(pa)), k=2)
    i1b, i2b = choices(range(len(pb)), k=2)

    if i1a > i2a:
        i1a, i2a = i2a, i1a

    if i1b > i2b:
        i1b, i2b = i2b, i1b
    
    return pa[:i1a] + pb[i1b:i2b] + pa[i2a:], pb[:i1b] + pa[i1a:i2a] + pb[i2b:]

def crossover(pa, pb):
    r = random()
    if r < 0.5:
        return twoPointCrossover(pa, pb)
    newpa = pa
    newpb = pb
    l = min(len(newpa), len(newpb))
    for i in range(l):
        if random() < 1 / l:
            newpa[i], newpb[i] = newpb[i], newpa[i]

    return newpa, newpb

def genetic_algorithm(t, n, initial_candidates, multiset, dictionary):
    _fitness = lambda x: fitness(x, deepcopy(multiset), dictionary)
    _tournament = lambda x: tournament(x, multiset, dictionary)

    popsize = 10
    elite = 4

    P = initial_candidates

    best = None
    start = time()
    while time() - start < t:
        allowed = [p for p in P if "".join(p) in dictionary and _fitness(p) != 0]
        # allowed = list(set(allowed))
        allowed.sort(key=lambda x: _fitness(x), reverse=True)

        for p in allowed:
            if best == None or _fitness(p) > _fitness(best):
                best = p
                last_best = time()

        Q = allowed[:elite]
        for _ in range((popsize - elite) // 2):
            p_a = _tournament(deepcopy(allowed))
            p_b = _tournament(deepcopy(allowed))
            c_a, c_b = crossover(deepcopy(p_a), deepcopy(p_b))
            Q.append(mutate(c_a, multiset, dictionary))
            Q.append(mutate(c_b, multiset, dictionary))
        P = Q

        if time() - last_best > log(t):
            break
    return best, _fitness(best)


def main():
    t, n, s = map(int, input().split())

    multiset = {}
    for _ in range(n):
        [char, value] = input().split()
        if char in multiset:
            multiset[char] = (multiset[char][0], multiset[char][1] + 1)
        else:
            multiset[char] = (int(value), 1)

    initial_candidates = []
    for _ in range(s):
        initial_candidates.append(list(input()))

    with open("dict.txt", "r") as f:
        content = f.readlines()
        dictionary = {}
        for word in content:
            dictionary[word[: len(word) - 1]] = ""

    result, qual = genetic_algorithm(t, n, initial_candidates, multiset, dictionary)
    print(qual)
    print("".join(result), file=stderr)


if __name__ == "__main__":
    main()
