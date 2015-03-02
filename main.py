#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module calculates the fastest path from a
starting point A to the finish point B using
the A*-algorithm
"""

from __future__ import print_function
import random
from multiprocessing import Pool


class Position():
    """
    This class represents a node in the A* algorithm
    Every position consists of a x- and y-value.

    Addition, comparison and copying methods are implemented
    """
    def __init__(self, x, y):
        self._xpos = x
        self._ypos = y

    def copy(self):
        return Position(self._xpos, self._ypos)

    def __add__(self, other):
        return Position(self.get_x() + other.get_x(), self.get_y() + other.get_y())

    def __sub__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        raise Exception("Multiplication not Implemented for Positions")

    def __div__(self, other):
        raise Exception("Division not implemented for Positions")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "({:}, {:})".format(self._xpos, self._ypos)

    def __abs__(self):
        return pow(self._xpos**2 + self._ypos**2, 0.5)

    def __lt__(self, other):
        if (self._xpos < other.get_x()) and (self._ypos < other.get_y()):
            return True
        return False

    def __le__(self, other):
        if (self._xpos <= other.get_x()) and (self._ypos <= other.get_y()):
            return True
        return False

    def __eq__(self, other):
        if (self._xpos == other.get_x()) and (self._ypos == other.get_y()):
            return True
        return False

    def __ne__(self, other):
        if (self._xpos != other.get_x()) or (self._ypos != other.get_y()):
            return True
        return False

    def __gt__(self, other):
        if (self._xpos > other.get_x()) and (self._ypos > other.get_y()):
            return True
        return False

    def __ge__(self, other):
        if (self._xpos >= other.get_x()) and (self._ypos >= other.get_y()):
            return True
        return False

    @staticmethod
    def random_valid():
        straight = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        diagonal = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        val = random.choice(straight + diagonal)
        return Position(val[0], val[1])

    def get_x(self):
        return self._xpos

    def get_y(self):
        return self._ypos


class Field():
    def __init__(self, xsize, ysize):
        self.data = [[0 for x in range(xsize)] for x in range(ysize)]

        for i in range(9):
            self.data[i][6] = 1

        for i in range(1, 10):
            self.data[i][10] = 1

        self.steps = []
        self.xsize = xsize
        self.ysize = ysize
        self.done = False
        self.path = []

        self.start = None
        self.end = None
        self.pos = None

    def set_start(self, start):
        self.start = start
        self.path.append(start)
        self.pos = start.copy()

    def set_end(self, end):
        self.end = end

    def possible(self, pos):
        if pos in self.path:
            return False

        if not Position(self.xsize, self.ysize) > pos >= Position(0, 0):
            return False

        if self.data[pos.get_y()][pos.get_x()] == 1:
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
            if new_pos not in self.path:
                if self.data[new_pos.get_y()][new_pos.get_x()] != 1:
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
        return sum([abs(step) for step in self.steps])

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
        for y_pos, row in enumerate(self.data):
            data += "|"
            for x_pos, field in enumerate(row):
                pos = Position(x_pos, y_pos)

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


def calc_best(cid):
    xmax = 20
    ymax = 10
    best = None
    results = []
    for i in range(50):
        f = Field(xmax, ymax)
        f.set_start(Position(0, 0))
        f.set_end(Position(xmax - 1, ymax - 1))

        while not f.done:
            f.go_random_step()

        if not best:
            best = f
            results.append(str(f))
        else:
            if f.cost() < best.cost():
                print("Child {:}: New {:} better than old {:}. {:} percent done"
                      .format(cid, f.cost(), best.cost(), 100 * i/200.0))
                best = f.copy()
                results.append(str(f))

    print("Child {:}: DONE".format(cid))
    for res in results:
        print(res)
        input()
    return best


def main():
    result = calc_best(0)
    print(result)


def main_parallel():
    best = None
    p = Pool(8)
    try:
        results = p.map(calc_best, range(8))
    except KeyboardInterrupt:
        p.terminate()
        p.join()
        return

    for result in results:
        if not best:
            best = result.copy()
        else:
            if result.cost() < best.cost():
                best = result.copy()

    print(best)

if __name__ == '__main__':
    main()
