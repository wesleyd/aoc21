#!/usr/bin/env python3

import difflib

from itertools import permutations
from heapdict import heapdict

example_input = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

def parse(input):
    maze = {}
    positions = []
    for y, line in enumerate(input.splitlines()):
        for x, c in enumerate(line):
            if c in ('A', 'B', 'C', 'D'):
                maze[(x,y)] = '.'
                positions.append((c, x, y))
            elif c in ('.', '#'):
                maze[(x,y)] = c
    return maze, tuple(sorted(positions))

def extents(maze):
    xlo, xhi = float('inf'), float('-inf')
    ylo, yhi = float('inf'), float('-inf')
    for x, y in maze.keys():
        if x < xlo: xlo = x
        if x > xhi: xhi = x
        if y < ylo: ylo = y
        if y > yhi: yhi = y
    return (xlo, xhi, ylo, yhi)

def unparse(maze, positions):
    lines = []
    xlo, xhi, ylo, yhi = extents(maze)
    for y in range(yhi+1):
        line = []
        for x in range(xhi+1):
            line.append(maze.get((x,y), ' '))
        lines.append(line)
    for (c, x, y) in positions:
        lines[y][x] = c
    return '\n'.join((''.join(line).rstrip() for line in lines))

def test_unparse():
    maze, positions = parse(example_input)
    got = unparse(maze, positions)
    #assert got == example_input, ''.join(difflib.unified_diff(got, example_input))
    assert got == example_input, (got, example_input)
test_unparse()

corridor_stops = {(1,1), (2,1), (4,1), (6,1), (8,1), (10,1), (11,1)}

def sign(x):
    return -1 if x < 0 else 1

def path_clear(occupied, begin, end):
    x1, y1 = begin
    x2, y2 = end
    for y in range(1, y1, 1):
        if (x1,y) in occupied:
            #print('  No, 1, occupied by:', occupied[(x1,y)])
            return False
    for x in range(x2, x1, sign(x1-x2)):
        if (x,1) in occupied:
            #print('  No, 2, occupied by:', occupied[(x,1)])
            return False
    for y in range(1, y2+1, 1):
        if (x2,y) in occupied:
            #print('  No, 3, occupied by:', occupied[(x2,y)])
            return False
    #print('  Yes')
    return True

def all_moves(positions, goalx):
    """yields all moves possible from positions towards goalx"""
    occupied = {}
    for (c,x,y) in positions:
        occupied[(x,y)] = c
    for (c,x,y) in positions:
        if y == 3 and x == goalx[c]:
            # We're home, we don't have to move.
            continue
        if y == 2 and x == goalx[c] and (c, x, 3) in positions:
            # We're home, we're not blocking an amphipod that wants out
            continue
        # We should move, if we can. Let's try moving home...
        if path_clear(occupied, (x,y), (goalx[c], 3)):
            yield (c, (x,y), (goalx[c], 3))
        elif path_clear(occupied, (x,y), (goalx[c], 2)) and (c, goalx[c], 3) in positions:
            # Move to the outer position : inner position is the same as us
            yield (c, (x,y), (goalx[c], 2))
        elif y > 1:
            # We can move to the corridor only if we're in a room
            for dest in corridor_stops:
                if path_clear(occupied, (x,y), dest):
                    yield (c, (x,y), dest)

def apply_move(positions, move):
    new_positions = []
    amphipod, a, z = move
    for (c, x, y) in positions:
        if (x, y) == a:
            if c != amphipod:
                raise Exception('bad amphipod %c v %c: move %s -> %s' % (c, amphipod, a, z))
        if c == amphipod and (x,y) == a:
            new_positions.append((c, z[0], z[1]))
            steps = (a[1] - 1) + abs(a[0] - z[0]) + (z[1] - 1)
        else:
            new_positions.append((c, x, y))
    return tuple(sorted(new_positions)), steps
assert apply_move( (('A', 1, 2), ('A', 2,3)),
                   ('A', (1, 2), (3, 4)) ) == ((('A', 2, 3), ('A', 3, 4)), 6)

amphipod_costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

def goalx_from_goal(goal):
    goalx = {}
    for (c, x, y) in goal:
        if c in goalx:
            assert goalx[c] == x
        goalx[c] = x
    return goalx

def dijkstra(positions, goal):
    goalx = goalx_from_goal(goal)
    q = heapdict()
    q[positions] = 0
    #prev = {}
    #prev[positions] = None
    while q:
        u, cost = q.popitem()
        if u == goal:
            return cost
        for move in all_moves(u, goalx):
            v, steps = apply_move(u, move)
            alt = cost + steps * amphipod_costs[move[0]]
            if alt < q.get(v, float('inf')):
                q[v] = alt
                #prev[v] = u
    return None

sorted_goal = (('A', 3, 2), ('A', 3, 3), ('B', 5, 2), ('B', 5, 3), ('C', 7, 2), ('C', 7, 3), ('D', 9, 2), ('D', 9, 3))

def find_cheapest(input):
    maze, positions = parse(input)
    cheapest = float('inf')
    cost = dijkstra(positions, sorted_goal)
    if cost < cheapest:
        cheapest = cost
    return cheapest

assert find_cheapest(example_input) == 12521

with open('inputs/day23.input') as f:
    print('Day 23 part 1 => %s' % find_cheapest(f.read()))
