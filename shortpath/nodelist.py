#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Nodelist(object):

    def __init__(self, *args):
        self.stor = dict()

        for node in args:
            self.append(node)

    def pop_min(self):
        try:
            best = min(self.stor.values())
            return self.stor.pop((best.x, best.y))
        except ValueError:
            return None

    def get(self, x, y):
        try:
            return self.stor[(x, y)]
        except KeyError:
            return None

    def append(self, o):
        self.stor[(o.x, o.y)] = o

    def __iter__(self):
        return self.stor.__iter__()

    def __len__(self):
        return len(self.stor)

    def __contains__(self, obj):
        return (obj.x, obj.y) in self.stor
