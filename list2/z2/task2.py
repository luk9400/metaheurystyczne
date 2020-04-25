#!/usr/bin/python

from time import time
from copy import deepcopy
from math import exp
from random import random, choice, randint
from sys import stderr

VALUES = [0, 32, 64, 128, 160, 192, 223, 255]


class Matrix:
    def __init__(self, n, m, k, blocks):
        self.height = n
        self.width = m
        self.k = k
        self.blocks = blocks

    def get(self, row, column):
        for block in self.blocks:
            if row in range(block.row, block.row + block.height) and column in range(
                block.column, block.column + block.width
            ):
                return block.value


class Block:
    def __init__(self, row, column, height, width, value):
        self.row = row
        self.column = column
        self.height = height
        self.width = width
        self.value = value


def quality(Mprim, M, n, m):
    return (1 / (n * m)) * sum(
        sum((M[i][j] - Mprim.get(i, j)) ** 2 for j in range(m)) for i in range(n)
    )


def initial_matrix(n, m, k):
    blocks = []
    k = k + 1

    for i in range(n // k):
        for j in range(m // k):
            block = Block(i * k, j * k, k, k, choice(VALUES))

            if block.row == (n // k - 1) * k:
                block.height += n % k

            if block.column == (m // k - 1) * k:
                block.width += m % k

            blocks.append(block)

    return Matrix(n, m, k - 1, blocks)


def change_intensity(M):
    block = choice(M.blocks)
    block.value = choice(VALUES)
    return M


def swap(M):
    block1 = choice(M.blocks)
    block2 = choice(M.blocks)
    block1.value, block2.value = block2.value, block1.value
    return M


def split(length, k):
    length = length - 2 * k
    if length > 0:
        len1 = length - randint(0, length)
        len2 = length - len1
    else:
        len1 = 0
        len2 = 0
    return len1 + k, len2 + k


def resize(M):
    block = choice(M.blocks)
    neighbour = None
    direction = None

    for b in M.blocks:
        if b is block:
            continue

        if b.row == block.row and b.height == block.height:
            if b.column + b.width == block.column:
                neighbour = b
                direction = "left"
            elif b.column == block.column + block.width:
                neighbour = b
                direction = "right"
            break

        if b.column == block.column and b.width == block.width:
            if b.row + b.height == block.row:
                neighbour = b
                direction = "up"
            elif b.row == block.row + block.height:
                neighbour = b
                direction = "down"
            break

    if neighbour:
        if direction in ["left", "right"]:
            width1, width2 = split(block.width + b.width, M.k)

            block.column = min(block.column, neighbour.column)
            block.width = width1

            neighbour.column = block.column + width1
            neighbour.width = width2
        else:
            height1, height2 = split(block.height + neighbour.height, M.k)

            block.row = min(block.row, neighbour.row)
            block.height = height1

            neighbour.row = block.row + height1
            neighbour.height = height2
    else:
        block.value = choice(VALUES)

    return M


def tweak(M):
    func = choice([change_intensity, resize])
    return func(M)


def decrease(t):
    return t * 0.99


def simulated_annealing(M, n, m, k, t):
    temp = 10 ** 8

    s = initial_matrix(n, m, k)
    best = s

    start = time()
    while time() - start < t and temp > 0:
        r = tweak(deepcopy(s))

        if quality(r, M, n, m) < quality(s, M, n, m) or random() < exp(
            (quality(s, M, n, m) - quality(r, M, n, m)) / temp
        ):
            s = r
        temp = decrease(temp)
        if quality(s, M, n, m) < quality(best, M, n, m):
            best = s
    return best


def print_matrix(M, n, m):
    for i in range(n):
        for j in range(m):
            print(M.get(i, j), "", end="", file=stderr)
        print("", file=stderr)


if __name__ == "__main__":
    t, n, m, k = map(int, input().split())

    matrix = []
    for _ in range(n):
        matrix.append(list(map(int, input().split())))

    res = simulated_annealing(matrix, n, m, k, t)
    print(quality(res, matrix, n, m))
    print_matrix(res, n, m)
