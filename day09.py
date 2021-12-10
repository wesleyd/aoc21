#!/usr/bin/env python3

import math

test_input = """\
2199943210
3987894921
9856789892
8767896789
9899965678
"""

def gridify(input):
    """Turns a multi-line string into a matrix of ints"""
    return [list(map(int, line)) for line in input.splitlines()]

def at(grid, row, col, dflt=9):
    if not (0 <= row and row < len(grid)):
        return dflt
    if not (0 <= col and col < len(grid[row])):
        return dflt
    return grid[row][col]

def lows(g):
    for row in range(len(g)):
        for col in range(len(g[row])):
            v = at(g, row, col)
            if v < at(g, row+1, col) and v < at(g, row, col+1) and v < at(g, row-1,col) and v < at(g, row, col-1):
                yield v

def risk(g):
    return sum(map(lambda x: x + 1, lows(g)))

assert risk(gridify(test_input)) == 15

with open('day09.input') as f:
    g = gridify(f.read())
    print('Day 9 Part 1 => %d' % risk(g))  # => 489

### Part 2

def basin_size(grid, row, col, visited=None):
    """How big is the basin near (row, col)?"""
    if not visited:
        visited = set()
    if at(grid, row, col) == 9:
        return 0
    if (row, col) in visited:
        return 0
    visited.add((row, col))
    size = 1
    size += basin_size(grid, row-1, col, visited)
    size += basin_size(grid, row+1, col, visited)
    size += basin_size(grid, row, col-1, visited)
    size += basin_size(grid, row, col+1, visited)
    return size

wants = {
    (0, 0): 3,
    (0, 9): 9,
    (2, 2): 14,
    (4, 9): 9,
}
for inp, want in wants.items():
    g = gridify(test_input)
    row, col = inp
    got = basin_size(g, row, col)
    if got != want:
        raise Exception('basin_size(%d,%d): got %d, want %d' % (row, col, got, want))

def low_points(g):
    for row in range(len(g)):
        for col in range(len(g[row])):
            v = at(g, row, col)
            if v < at(g, row+1, col) and v < at(g, row, col+1) and v < at(g, row-1,col) and v < at(g, row, col-1):
                yield (row, col)

def basins(g):
    for row, col in low_points(g):
        yield basin_size(g, row, col)

def mul3basins(g):
    bb = list(basins(g))
    bb.sort()
    return math.prod(bb[-3:])

assert mul3basins(gridify(test_input)) == 1134

with open('day09.input') as f:
    g = gridify(f.read())
    print('Day 9 part 2 => %d' % mul3basins(g))
