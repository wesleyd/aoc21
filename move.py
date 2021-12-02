#!/usr/bin/env python3

import collections.namedtuple

Position = collections.namedtuple("Position", "horizontal", "depth")



def move(pos, cmd):
    pieces = split(cmd)
    direction, steps = pieces[0], int(pieces[1])
