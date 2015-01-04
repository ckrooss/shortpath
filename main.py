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


class Field():
    def __init__(self, xsize, ysize):
        self.data = [[0 for x in range(xsize)] for x in range(ysize)]
        self.steps = []
        self.xsize = xsize
        self.ysize = ysize
        self.done = False
        self.i = 0

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end

    def possible(self, pos):
        if not (Position(self.xsize, self.ysize) > pos >= Position(0, 0)):
            return False

        x, path = self.calc_state()
        if pos in path:
            return False

        return True

    def deadlock(self):
        pos, path = self.calc_state()

        if (not self.possible(pos + Position(0, 1)) and
                not self.possible(pos + Position(0, -1)) and
                not self.possible(pos + Position(1, 0)) and
                not self.possible(pos + Position(-1, 0))):
            return True

        return False

    def calc_state(self):
        self.path = [self.start]
        pos = self.start.copy()
        for step in self.steps:
            pos += step
            path.append(pos)

        return pos, path

    def go_step(self, step):
        if (abs(step) <= 1):
            pos, path = self.calc_state()

            if pos == self.end:
                self.done = True
                return True

            if Position(self.xsize, self.ysize) > (pos + step) >= Position(0, 0):
                if (pos + step not in path):
                    self.steps.append(step)
                    self.i = 0
                    return True
        self.i += 1
        return False

    def go_random_step(self):
        while not self.go_step(Position(random.randint(-1, 1), random.randint(-1, 1))):
            if self.deadlock():
                self.restart()

            #if self.i > 10:
                #import pdb;pdb.set_trace()

    def restart(self):
        self.steps = []

    def cost(self):
        return len(self.steps)

    def copy(self):
        copy = Field(self.xsize, self.ysize)
        copy.steps = self.steps[:]
        return copy

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        data = ""
        data += "-" * (len(self.data) + 2)
        data += "\n"
        for y, row in enumerate(self.data):
            data += "|"
            for x, field in enumerate(row):
                pos = Position(x, y)
                cur, path = self.calc_state()

                if pos == cur:
                    data += "X"
                elif pos in path:
                    data += "."
                else:
                    data += " "
            data += "|\n"

        data += "-" * (len(self.data) + 2)
        data += "\n"
        return data

xmax = 5
ymax = 5

best = None

for i in range(2000):
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

print(f)
