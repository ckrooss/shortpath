#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import randint
if __name__ == "__main__":
    from node import Node
    from nodelist import Nodelist
else:
    from .node import Node
    from .nodelist import Nodelist

Node.xmax = 30
Node.ymax = 15


def gen_obstacles(xmax: int, ymax: int) -> Nodelist:
    obstacles = Nodelist()

    def ao(x, y):
        o = Node(x, y)
        obstacles.append(o)

    for _ in range(2):
        ao(randint(-xmax, xmax), randint(-ymax, ymax))

    for y in range(-ymax, ymax):
        ao(0, y + 1)

    for y in range(-ymax, ymax + 1):
        ao(-xmax, y)

    for k, j in zip(range(1, xmax), range(ymax)):
        ao(xmax - k, j - (ymax // 3))

    return obstacles


def find_path(ziel: Node, openlist: Nodelist, closedlist: Nodelist, obstacles: Nodelist) -> bool:
    while openlist:
        current_node = openlist.pop_min()

        if current_node == ziel:
            ziel.pre = current_node
            return True

        closedlist.append(current_node)

        current_node.expand_node(ziel, openlist, closedlist, obstacles)

    return False


def main():
    start = Node(-Node.xmax, Node.ymax)
    ziel = Node(Node.xmax, Node.ymax)

    while True:
        # List of elements that form the optimal way
        optimal_path = Nodelist()

        # Openlist: Path elements that have not been fully evaluated and might be good
        openlist = Nodelist(start)

        # Closedlist: Path elements that have been fully evaluated
        closedlist = Nodelist()

        # Blocking the path
        obstacles = gen_obstacles(Node.xmax, Node.ymax)

        if find_path(ziel, openlist, closedlist, obstacles):
            Node.select_optimal_path(ziel, optimal_path)
            Node.printf(start, ziel, optimal_path, openlist, closedlist, obstacles)
            break
        else:
            Node.printf(start, ziel, optimal_path, openlist, closedlist, obstacles)
            raise Exception()

if __name__ == '__main__':
    main()
