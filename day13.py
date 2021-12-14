#!/usr/bin/env python3

test_input = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

def parse(input):
    points, instructions = input.split('\n\n')
    graph = set()
    folds = []
    for p in points.splitlines():
        l, r = p.split(',')
        x, y = int(l), int(r)
        graph.add((x,y))
    for a in instructions.splitlines():
        l, r = a.split('=')
        folds.append((l[-1], int(r)))
    return graph, folds

parse(test_input)

def fold1(graph, fold):
    axis, n = fold
    g2 = set()
    for x, y in graph:
        if axis == 'y':
            if y < n:
                g2.add((x, y))
            else:
                g2.add((x, 2*n-y))
        elif axis == 'x':
            if x < n:
                g2.add((x, y))
            else:
                g2.add((2*n-x, y))
        else:
            raise('bad axis %s' % axis)
    return g2

def display(graph):
    maxx, maxy = 0, 0
    for x, y in graph:
        if x > maxx:
            maxx = x
        if y > maxy:
            maxy = y
    for y in range(maxy+1):
        for x in range(maxx+1):
            if (x,y) in graph:
                print('#', end='')
            else:
                print('.', end='')
        print()

def foldall(graph, folds):
    for fold in folds:
        graph = fold1(graph, fold)
    return graph

#graph, folds = parse(test_input)
#display(graph)
#display(foldall(graph, folds))

graph, folds = parse(test_input)
got = len(fold1(graph, folds[0]))
want = 17
assert got == want, 'first fold to test input: got %d, want %d' % (got, want)


with open('inputs/day13.input') as f:
    graph, folds = parse(f.read())
    g2 = fold1(graph, folds[0])
    print('Day 13, part 1 => %d' % len(g2))  # => 621

### Part 2

with open('inputs/day13.input') as f:
    graph, folds = parse(f.read())
    print('Day 13, part 2 ...')
    display(foldall(graph, folds))  # => HKUJGAJZ
