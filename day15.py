#!/usr/bin/env python

from heapdict import heapdict

test_input = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

def parse(input):
    grid = []
    for line in input.splitlines():
        grid.append([int(c) for c in line])
    return grid

def neighbors(grid, p):
    row, col = p
    if row > 0:
        yield (row-1, col)
    if row < len(grid[row])-1:
        yield (row+1, col)
    if col > 0:
        yield (row, col-1)
    if col < len(grid)-1:
        yield (row, col+1)

def walk(grid, target=None, start=(0,0)):
    if target == None:
        target = (len(grid)-1, len(grid[0])-1)
    q = heapdict()
    q[start] = 0
    prev = {}
    dist = {}
    dist[start] = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            v = (row, col)
            if v != start:
                prev[v] = None
                dist[v] = 1_000_000_000
            q[v] = 1_000_000_000  # A very big number indeed!
    while q:
        u, _ = q.popitem()
        for v in neighbors(grid, u):
            alt = dist[u] + grid[v[0]][v[1]]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                q[v] = alt
    #return dist, prev
    return dist[target]  # We could probably do this earlier...

got = walk(parse(test_input))
want = 40
assert got == want, 'least risky path through test_input: got %d, want %d' % (got, want)

with open('inputs/day15.input') as f:
    grid = parse(f.read())
    best = walk(grid)
    print("Day 15, part 1 => %d" % best)
