#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
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

    for _ in range(100):
        ao(randint(-xmax, xmax), randint(-ymax, ymax))

    for y in range(-ymax, ymax):
        ao(0, y + 1)

    for y in range(-ymax, ymax + 1):
        ao(-xmax, y)

    for k, j in zip(range(xmax), range(ymax)):
        ao(xmax - k, j - 5)

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


def main(start, ziel):
    while True:
        optimal_path = Nodelist()
        openlist = Nodelist(start)
        closedlist = Nodelist()

        obstacles = gen_obstacles(Node.xmax, Node.ymax)

        if find_path(ziel, openlist, closedlist, obstacles):
            Node.select_optimal_path(ziel, optimal_path)
            Node.printf(start, ziel, optimal_path, openlist, closedlist, obstacles)
            break

if __name__ == '__main__':
    start_node = Node(-30, 15)
    ziel_node = Node(Node.xmax, Node.ymax)

    main(start_node, ziel_node)
