#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from termcolor import cprint


class Node:
    xmax = None
    ymax = None

    def __init__(self, x: int, y: int, f=0):
        assert Node.xmax, "need to define Node.xmax"
        assert Node.ymax, "need to define Node.ymax"

        if abs(x) > Node.xmax:
            raise ValueError("Invalid param for x: %s" % x,
                             "Must be %s < x < %s" % (-Node.xmax, Node.xmax))

        if abs(y) > Node.ymax:
            raise ValueError("Invalid param for y: %s" % y,
                             "Must be %s < y < %s" % (-Node.ymax, Node.ymax))

        self.x = x
        self.y = y
        self.f = f
        self.g = 0
        self.pre = None
        self.successors = []

    @staticmethod
    def select_optimal_path(ziel, optimal_path) -> None:
        c = ziel

        while c:
            optimal_path.append(c)
            c = c.pre

    @staticmethod
    def printf(start, ziel, optimal_path, openlist, closedlist, obstacles) -> None:
        print("\n ╔", end="")
        print("═" * (2 * Node.xmax + 1), sep="", end="")
        print("╗")
        for y in range(-Node.ymax, Node.ymax + 1):
            print(" ║", sep="", end="")
            for x in range(-Node.xmax, Node.xmax + 1):
                if Node(x, y) == start:
                    cprint("A", "red", sep="", end="")
                elif Node(x, y) == ziel:
                    cprint("Z", "red", sep="", end="")
                elif optimal_path.get(x, y):
                    cprint("O", "green", sep="", end="")
                elif openlist.get(x, y):
                    print("X", sep="", end="")
                elif closedlist.get(x, y):
                    cprint("O", "yellow", sep="", end="")
                elif obstacles.get(x, y):
                    cprint("#", "blue", sep="", end="")
                else:
                    print(" ", sep="", end="")
            print("║ \n", sep="", end="")
        print(" ╚", end="")
        print("═" * (2 * Node.xmax + 1), sep="", end="")
        print("╝\n")

    def valid_step(self, x_step: int, y_step: int, obstacles) -> int:
        if abs(x_step**2 + y_step**2) > 1:
            return False

        new_x = self.x + x_step
        new_y = self.y + y_step

        if (x_step == 0) and (y_step == 0):
            return False

        if obstacles.get(new_x, new_y) is not None:
            return False

        if any([new_x > Node.xmax,
                new_x < -Node.xmax,
                new_y > Node.ymax,
                new_y < -Node.ymax]):
            return False

        return True

    def expand_node(self, ziel, openlist, closedlist, obstacles) -> None:
        for xstep in [-1, 0, 1]:
            for ystep in [-1, 0, 1]:
                if self.valid_step(xstep, ystep, obstacles):
                    self.successors.append(Node(self.x + xstep, self.y + ystep))

        for successor in self.successors:
            if successor in closedlist:
                continue

            # g Wert für den neuen Weg berechnen: g Wert des Vorgängers plus
            # die Kosten der gerade benutzten Kante
            tentative_g = self.g + Node.dist(self, successor)

            # wenn der Nachfolgeknoten bereits auf der Open List ist,
            # aber der neue Weg nicht besser ist als der alte - tue nichts
            if successor in openlist:
                successor = openlist.get(successor.x, successor.y)
                if tentative_g >= successor.g:
                    continue

            # Vorgängerzeiger setzen und g Wert merken
            successor.pre = self
            successor.g = tentative_g

            # f Wert des Knotens in der Open List aktualisieren
            # bzw. Knoten mit f Wert in die Open List einfügen
            f = tentative_g + Node.dist(ziel, successor)
            successor.f = f

            openlist.append(successor)

    @staticmethod
    def dist(a, b) -> int:
        return (b.y - a.y) ** 2 + (b.x - a.x) ** 2

    def __eq__(self, other):
        return all((self.x == other.x, self.y == other.y))

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __repr__(self):
        return "NODE(x: {:}, y: {:}, f: {:}, g: {:}".format(self.x, self.y, self.f, self.g)

    def __hash__(self):
        return hash(str(self.x) + str(self.y))
