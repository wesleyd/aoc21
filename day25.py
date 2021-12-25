#!/usr/bin/env python3

import copy

example_input = """\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""

def parse(input):
    grid = []
    for line in input.splitlines():
        line = line.strip()
        if not line: continue
        grid.append([c for c in line])
    if len(grid) == 0:
        raise Exception('empty grid')
    for y in range(1, len(grid)):
        if len(grid[y]) != len(grid[0]):
            raise Exception('wrong length line %d: %d not %d' % (y, len(grid[y]), len(grid[0])))
    return grid

def unparse(grid):
    return '\n'.join([''.join(row) for row in grid])
assert unparse(parse(example_input)) + '\n' == example_input

def at(grid, x, y):
    y %= len(grid)
    x %= len(grid[y])
    return grid[y][x]

def move_right(grid):
    if isinstance(grid, str): raise Exception('bad grid')
    nmoves = 0
    for y in range(len(grid)):
        left = grid[y][0]
        right = grid[y][-1]
        x = 0
        while x < len(grid[y])-1:
            if grid[y][x] == '>' and grid[y][x+1] == '.':
                grid[y][x] = '.'
                grid[y][x+1] = '>'
                x += 1
                nmoves += 1
            x += 1
        if right == '>' and left == '.':
            grid[y][0] = '>'
            grid[y][-1] = '.'
            nmoves += 1
    return nmoves
def test_move_right():
    grid = parse('...>>>>>...')
    move_right(grid)
    assert unparse(grid) == '...>>>>.>..'
    move_right(grid)
    assert unparse(grid) == '...>>>.>.>.'
    move_right(grid)
    assert unparse(grid) == '...>>.>.>.>'
    move_right(grid)
    assert unparse(grid) == '>..>.>.>.>.', unparse(grid)
    grid = parse('>.........>')
    move_right(grid)
    assert unparse(grid) == '.>........>'
test_move_right()

def move_down(grid):
    nmoves = 0
    if isinstance(grid, str): raise Exception('bad grid')
    for x in range(len(grid[0])):
        top = grid[0][x]
        bottom = grid[-1][x]
        y = 0
        while y < len(grid)-1:
            if grid[y][x] == 'v' and grid[y+1][x] == '.':
                grid[y][x] = '.'
                grid[y+1][x] = 'v'
                y += 1
                nmoves += 1
            y += 1
        if bottom == 'v' and top == '.':
            grid[0][x] = 'v'
            grid[-1][x] = '.'
            nmoves += 1
    return nmoves

def move(grid):
    return move_right(grid) + move_down(grid)
def test_move():
    grid = parse("""\
        ...>...
        .......
        ......>
        v.....>
        ......>
        .......
        ..vvv.. """)
    move(grid)
    assert grid == parse("""\
        ..vv>..
        .......
        >......
        v.....>
        >......
        .......
        ....v.. """)
    move(grid)
    assert grid == parse("""\
        ....v>.
        ..vv...
        .>.....
        ......>
        v>.....
        .......
        ....... """)
    move(grid)
    assert grid == parse("""\
        ......>
        ..v.v..
        ..>v...
        >......
        ..>....
        v......
        ....... """)
    move(grid)
    assert grid == parse("""\
        >......
        ..v....
        ..>.v..
        .>.v...
        ...>...
        .......
        v...... """)
test_move()

def test_move2():
    grid = parse("""
        v...>>.vv>
        .vv>>.vv..
        >>.>v>...v
        >>v>>.>.v.
        v>v.vv.v..
        >.>>..v...
        .vv..>.>v.
        v.v..>>v.v
        ....v..v.> """)
    move(grid)
    assert grid == parse("""
        ....>.>v.>
        v.v>.>v.v.
        >v>>..>v..
        >>v>v>.>.v
        .>v.v...v.
        v>>.>vvv..
        ..v...>>..
        vv...>>vv.
        >.v.v..v.v """)
    move(grid)
    assert grid == parse("""
        >.v.v>>..v
        v.v.>>vv..
        >v>.>.>.v.
        >>v>v.>v>.
        .>..v....v
        .>v>>.v.v.
        v....v>v>.
        .vv..>>v..
        v>.....vv. """)
    for i in range(55):
        move(grid)
    assert grid == parse("""
        ..>>v>vv..
        ..v.>>vv..
        ..>>v>>vv.
        ..>>>>>vv.
        v......>vv
        v>v....>>v
        vvv.....>>
        >vv......>
        .>v.vv.v.. """)
test_move2()

def stops(grid):
    n = 1
    while move(grid) > 0:
        n += 1
    return n
assert stops(parse(example_input)) == 58

with open('inputs/day25.input') as f:
    print('Day25 part 1 => %d' % stops(parse(f.read())))
