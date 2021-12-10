#!/usr/bin/env python

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

def lows(input):
    g = gridify(input)
    ll = []
    for row in range(len(g)):
        for col in range(len(g[row])):
            v = at(g, row, col)
            if v < at(g, row+1, col) and v < at(g, row, col+1) and v < at(g, row-1,col) and v < at(g, row, col-1):
                ll.append(v)
    return ll

def risk(input):
    return sum(map(lambda x: x + 1, lows(input)))

assert risk(test_input) == 15

with open('day09.input') as f:
    print('Day 9 Part 1 =>', risk(f.read()))  # => 489
