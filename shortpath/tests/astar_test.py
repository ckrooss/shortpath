#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from shortpath.nodelist import Nodelist
from shortpath.node import Node
from shortpath.astar import gen_obstacles, main

Node.xmax = 10
Node.ymax = 10


class NodelistTests(unittest.TestCase):

    def test_Nodelist(self):
        nl = Nodelist()
        self.assertIsNotNone(nl)

    def test_NodelistInit(self):
        nl = Nodelist(Node(1, 1))
        self.assertEqual(len(nl), 1)
        self.assertTrue(Node(1, 1) in nl)

    def test_NodelistAppend(self):
        nl = Nodelist()
        n = Node(1, 1)

        nl.append(n)
        self.assertEqual(len(nl), 1)
        self.assertTrue(n in nl)

    def test_NodelistMin(self):
        nl = Nodelist(Node(1, 2, 2), Node(1, 3, 1), Node(1, 4, 2), Node(1, 5, 1), Node(1, 6, 3))
        self.assertEqual(len(nl), 5)

        self.assertEqual(nl.pop_min().f, 1)
        self.assertEqual(len(nl), 4)

        self.assertEqual(nl.pop_min().f, 1)
        self.assertEqual(len(nl), 3)

        self.assertEqual(nl.pop_min().f, 2)
        self.assertEqual(len(nl), 2)

    def test_Nodelistget(self):
        nl = Nodelist(Node(1, 2, 2), Node(1, 3, 1), Node(1, 4, 2), Node(1, 5, 1), Node(1, 6, 3))
        n = nl.get(x=1, y=5)
        self.assertEqual(n.x, 1)
        self.assertEqual(n.y, 5)

        self.assertIsNone(nl.get(25, 29))


class NodeTests(unittest.TestCase):

    def test_Node(self):
        n = Node(1, 2)
        self.assertIsNotNone(n)
        self.assertEqual(n.x, 1)
        self.assertEqual(n.y, 2)

        print(str(n))

    def test_NodeInvalid(self):
        self.assertRaises(ValueError, Node, -1, 200)

    def test_NodeComparison(self):
        n1 = Node(5, 3, f=4)
        n2 = Node(2, 9, f=2)
        n3 = Node(10, 1, f=12)

        self.assertTrue(n1 > n2)
        self.assertTrue(n2 < n3)
        self.assertTrue(n2 < n3)

    def test_NodeValidStep(self):
        n = Node(10, 10)
        obstacle = Node(10, 9)
        step_1 = n.valid_step(0, -1, Nodelist(obstacle))
        step_2 = n.valid_step(-1, 0, Nodelist(obstacle))
        step_3 = n.valid_step(1, 1, Nodelist(obstacle))

        self.assertFalse(step_1, "Cannot move on obstacle")
        self.assertTrue(step_2, "Can move next to obstacle")
        self.assertFalse(step_3, "Cannot exit max range")


class AstarTests(unittest.TestCase):

    def test_Obstacles(self):
        ob = gen_obstacles(Node.xmax, Node.ymax)
        self.assertTrue(len(ob) > 0)

    def test_Main(self):
        main()
