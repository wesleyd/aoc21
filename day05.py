#!/usr/bin/env python3

import collections
import re

day5_test_input = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

def parse(input):
    lines = []
    for line in input.splitlines():
        lines.append(list(map(int, re.split(r'[^0-9]+', line))))
    return lines

want = [[0,9,5,9],[8,0,0,8],[9,4,3,4],[2,2,2,1],[7,0,7,4],[6,4,2,0],[0,9,2,9],[3,4,1,4],[0,0,8,8],[5,5,8,2]]
got = parse(day5_test_input)
if got != want:
    raise Exception('parse:\n  got %s\n want %s' %(got, want))

def straight(lines):
    mesh = collections.defaultdict(int)
    for line in lines:
        x1,y1,x2,y2 = line
        if x1 == x2:
            y = min(y1,y2)
            while y <= max(y1,y2):
                mesh[(x1,y)] += 1
                y += 1
        elif y1 == y2:
            x = min(x1,x2)
            while x <= max(x1,x2):
                mesh[(x,y1)] += 1
                x += 1
        else:
            True
            # print('Skipping diagonal (%d,%d) -> (%d,%d)' % (x1,y1,x2,y2))
    return mesh

def stringify_mesh(mesh):
    s = ''
    maxx, maxy = 0, 0
    for k in mesh.keys():
        x,y = k
        if x > maxx:
            maxx = x
        if y > maxy:
            maxy = y
    for y in range(maxy+1):
        for x in range(maxx+1):
            v = mesh[(x,y)]
            if v > 0:
                s += '%d' % mesh[(x,y)]
            else:
                s += '.'
        s += '\n'
    return s


lines = parse(day5_test_input)
mesh = straight(lines)
got = stringify_mesh(mesh)
want = """\
.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
"""
if got != want:
    raise Exception('stringify_mesh:\n\ngot:\n%s\nwant:\n%s\n' %(got, want))

def noverlaps(mesh):
    n = 0
    for k, v in mesh.items():
        if v > 1:
            n += 1
    return n

lines = parse(day5_test_input)
mesh = straight(lines)
got = noverlaps(mesh)
if got != 5:
    raise Exception('test mesh has %d overlaps, want 5' % got)

with open("inputs/day05.input") as f:
    day5_input = f.read()
    day5_lines = parse(day5_input)
    day5_mesh = straight(day5_lines)
    print('Day 5 part 1 :: num overlaps => %d' % noverlaps(day5_mesh))  # => 4873

### Part 2

def sign(z):
    if z < 0:
        return -1
    if z > 0:
        return +1
    return 0

def diangley(lines):
    """Like straight, but include diagonals at pi/4."""
    mesh = collections.defaultdict(int)
    for line in lines:
        x1,y1,x2,y2 = line
        if x1 == x2:
            y = min(y1,y2)
            while y <= max(y1,y2):
                mesh[(x1,y)] += 1
                y += 1
        elif y1 == y2:
            x = min(x1,x2)
            while x <= max(x1,x2):
                mesh[(x,y1)] += 1
                x += 1
        elif abs(y2 - y1) == abs(x2 - x1):
            dx = sign(x2-x1)
            dy = sign(y2-y1)
            x, y = x1, y1
            #print("(%d,%d) -> (%d,%d) @(%d,%d)" % (x1, y1, x2, y2, dx, dy))
            done = False
            while True:
                #print("Setting (%d,%d)" % (x,y))
                mesh[(x,y)] += 1
                x += dx
                y += dy
                if done:
                    break
                if x == x2 and y == y2:
                    done = True
        else:
            raise Exception('Skipping weird diagonal (%d,%d) -> (%d,%d)' % (x1,y1,x2,y2))
    return mesh


lines = parse(day5_test_input)
mesh = diangley(lines)
got = stringify_mesh(mesh)
want = """\
1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
"""
if got != want:
    raise Exception('stringify_mesh:\n\ngot:\n%s\nwant:\n%s\n' % (got, want))

got = noverlaps(mesh)
if got != 12:
    raise Exception('test mesh has %d overlaps, want 12' % got)

with open("inputs/day05.input") as f:
    day5_input = f.read()
    day5_lines = parse(day5_input)
    day5_mesh = diangley(day5_lines)
    print('Day 5 part 2 :: num overlaps => %d' % noverlaps(day5_mesh))  # => 19472
