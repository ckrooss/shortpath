#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import random


class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Position(self.x, self.y)

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        raise NotImplementedError("Multiplication not Implemented for Positions")

    def __div__(self, other):
        raise NotImplementedError("Division not implemented for Positions")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "({:}, {:})".format(self.x, self.y)

    def __abs__(self):
        return self.x**2 + self.y**2

    def __lt__(self, other):
        if (self.x < other.x) and (self.y < other.y):
            return True
        return False

    def __le__(self, other):
        if (self.x <= other.x) and (self.y <= other.y):
            return True
        return False

    def __eq__(self, other):
        if (self.x == other.x) and (self.y == other.y):
            return True
        return False

    def __ne__(self, other):
        if (self.x != other.x) or (self.y != other.y):
            return True
        return False

    def __gt__(self, other):
        if (self.x > other.x) and (self.y > other.y):
            return True
        return False

    def __ge__(self, other):
        if (self.x >= other.x) and (self.y >= other.y):
            return True
        return False

    @staticmethod
    def random_valid():
        val = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        return Position(val[0], val[1])


class Field():
    def __init__(self, xsize, ysize):
        self.data = [[0 for x in range(xsize)] for x in range(ysize)]
        self.data[0][3] = 1
        self.data[1][3] = 1
        self.data[2][3] = 1
        self.data[3][3] = 1
        self.steps = []
        self.xsize = xsize
        self.ysize = ysize
        self.done = False
        self.path = []
        self.steps = []

    def set_start(self, start):
        self.start = start
        self.path.append(start)
        self.pos = start.copy()

    def set_end(self, end):
        self.end = end

    def possible(self, pos):
        if pos in self.path:
            return False

        if not (Position(self.xsize, self.ysize) > pos >= Position(0, 0)):
            return False

        if self.data[pos.y][pos.x] == 1:
            return False

        return True

    def deadlock(self):
        if (self.possible(self.pos + Position(0, 1)) or
                self.possible(self.pos + Position(0, -1)) or
                self.possible(self.pos + Position(1, 0)) or
                self.possible(self.pos + Position(-1, 0))):
            return False

        return True

    def go_step(self, step):
        if self.pos == self.end:
            self.done = True
            return True

        new_pos = self.pos + step
        if Position(self.xsize, self.ysize) > new_pos >= Position(0, 0):
            if (new_pos not in self.path):
                if self.data[new_pos.y][new_pos.x] != 1:
                    self.steps.append(step)
                    self.pos += step
                    self.path.append(self.pos)
                    return True
        return False

    def go_random_step(self):
        while not self.go_step(Position.random_valid()):
            if self.deadlock():
                self.restart()

    def restart(self):
        self.steps = []
        self.path = [self.start]
        self.pos = self.start.copy()

    def cost(self):
        cost = 0
        for step in self.steps:
            cost += abs(step)

        return cost

    def copy(self):
        copy = Field(self.xsize, self.ysize)
        copy.steps = self.steps[:]
        copy.path = self.path[:]
        copy.pos = self.pos
        return copy

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        data = ""
        data += "-" * (self.xsize + 2)
        data += "\n"
        for y, row in enumerate(self.data):
            data += "|"
            for x, field in enumerate(row):
                pos = Position(x, y)

                if pos == self.pos:
                    data += "X"
                elif pos in self.path:
                    data += "."
                elif field == 1:
                    data += "="
                else:
                    data += " "
            data += "|\n"

        data += "-" * (self.xsize + 2)
        data += "\n"
        return data

xmax = 15
ymax = 5

best = None

for i in range(500):
    f = Field(xmax, ymax)
    f.set_start(Position(0, 0))
    f.set_end(Position(xmax - 1, ymax - 1))

    while not f.done:
        f.go_random_step()

    if not best:
        best = f
    else:
        if f.cost() < best.cost():
            print("new {:} better than old {:}".format(f.cost(), best.cost()))
            best = f.copy()

print(best)
print(best.steps)
