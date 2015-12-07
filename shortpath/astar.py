#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import randint
from shortpath.node import Node
from shortpath.nodelist import Nodelist

Node.xmax = 30
Node.ymax = 15


def gen_obstacles(xmax, ymax):
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


def find_path(ziel, openlist, closedlist, obstacles):
    while openlist:
        currentNode = openlist.pop_min()

        if currentNode == ziel:
            ziel.pre = currentNode
            return True

        closedlist.append(currentNode)

        currentNode.expandNode(ziel, openlist, closedlist, obstacles)

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
