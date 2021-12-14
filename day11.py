#!/usr/bin/env python3

test_input = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

def parse(input):
    grid = []
    for line in input.splitlines():
        grid.append([int(c) for c in line])
    return grid

def stringify(grid):
    return '\n'.join([''.join(map(str, line)) for line in grid]) + '\n'

assert stringify(parse(test_input)) == test_input

def ginc(grid, row, col):
    if 0 <= row and row < len(grid):
        if 0 <= col and col < len(grid[row]):
            grid[row][col] += 1

def step(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            grid[row][col] += 1
    flashes = set()
    while True:
        changed = False
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] > 9 and (row, col) not in flashes:
                    changed = True
                    flashes.add((row, col))
                    ginc(grid, row-1, col-1)
                    ginc(grid, row-1, col)
                    ginc(grid, row-1, col+1)
                    ginc(grid, row, col-1)
                    ginc(grid, row, col+1)
                    ginc(grid, row+1, col-1)
                    ginc(grid, row+1, col)
                    ginc(grid, row+1, col+1)
        if not changed:
            break
    for row, col in flashes:
        grid[row][col] = 0
    return len(flashes)

# Smaller example...
step0 = """\
11111
19991
19191
19991
11111
"""
g = parse(step0)
step(g)
want1 = """\
34543
40004
50005
40004
34543
"""
got1 = stringify(g)
assert got1 == want1, 'after step 1:\n got:\n%s\nwant:\n%s' % (got1, want1)
step(g)
want2 = """\
45654
51115
61116
51115
45654
"""
got2 = stringify(g)
assert got2 == want2, 'after step 1:\n got:\n%s\nwant:\n%s' % (got2, want2)

# Bigger example...
step0 = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
g = parse(step0)
step(g)
want1 = """\
6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637
"""
got1 = stringify(g)
assert got1 == want1, 'after step 1:\n got:\n%s\nwant:\n%s' % (got1, want1)
step(g)
want2 = """\
8807476555
5089087054
8597889608
8485769600
8700908800
6600088989
6800005943
0000007456
9000000876
8700006848
"""
got2 = stringify(g)
assert got2 == want2, 'after step 2:\n got:\n%s\nwant:\n%s' % (got2, want2)
step(g)
want3 = """\
0050900866
8500800575
9900000039
9700000041
9935080063
7712300000
7911250009
2211130000
0421125000
0021119000
"""
got3 = stringify(g)
assert got3 == want3, 'after step 3:\n got:\n%s\nwant:\n%s' % (got3, want3)

def stepN(grid, nsteps):
    nflashes = 0
    for i in range(nsteps):
        nflashes += step(grid)
    return nflashes

step0 = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
g = parse(step0)
got = stepN(g, 100)
want = 1656
assert got == want, "Wrong number of flashes after 100 steps: got %d, want %d" % (got, want)

with open('inputs/day11.input') as f:
    g = parse(f.read())
    nflashes = stepN(g, 100)
    print('Day 11, part 1 => %d' % nflashes)  # => 1642

### Part 2

def stepSync(grid):
    """Keep stepping until all octopuses flash!"""
    noctopuses = len(grid) * len(grid[0])
    n = 1
    while True:
        nflashes = step(grid)
        if nflashes == noctopuses:
            return n
        n += 1

g = parse(test_input)
got = stepSync(g)
want = 195
assert got == want, "stepSync: got %d, want %d" % (got, want)

with open('inputs/day11.input') as f:
    g = parse(f.read())
    nsteps = stepSync(g)
    print('Day 11, part 2 => %d' % nsteps)  # => 320
