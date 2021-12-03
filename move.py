#!/usr/bin/env python3

from collections import namedtuple

### Day 2

# Part 1

Position = namedtuple("Position", ["horizontal", "depth"])
origin = Position(0,0)

def move(cmd, pos=origin):
    pieces = cmd.split()
    direction, steps = pieces[0], int(pieces[1])
    horizontal, depth = pos
    if direction == 'forward':
        horizontal += steps
    elif direction == 'down':
        depth += steps
    elif direction == 'up':
        depth -= steps
    return Position(horizontal, depth)

day2_test_input = [
    'forward 5',
    'down 5',
    'forward 8',
    'up 3',
    'down 8',
    'forward 2',
]

def moves(cmds, pos=origin):
    for cmd in cmds:
        pos = move(cmd, pos)
    return pos

got = moves(day2_test_input)
want = Position(15,10)
if got != want:
    raise Exception('Bad moves: got %s want %s' % (got, want))

def PosMul(pos):
    return pos.horizontal * pos.depth

f = open('day02.input')
day2_input = f.striplines()
f.close()
day2a = moves(day2_input)

# => (2165,933) *=> 20199445  <-- Wrong!
print('Day 2 Part 1 :: %s => %s' % (day2a, PosMul(day2a))) 

# Part 2

class Location:
    def __init__(self):
        self.horizontal = 0
        self.depth = 0
        self.aim = 0
    def move(self, cmd):
        pieces = cmd.split()
        direction, steps = pieces[0], int(pieces[1])
        if direction == 'forward':
            self.horizontal += steps
            self.depth += steps * self.aim
        elif direction == 'down':
            self.aim += steps
        elif direction == 'up':
            self.aim -= steps
        else:
            raise Exception('bad direction %s in cmd %s' % (direction, cmd))
    def moves(self, cmds):
        for cmd in cmds:
            self.move(cmd)
    def mult(self):
        return self.horizontal * self.depth

loc = Location()
loc.moves(day2_test_input)
got = loc.mult()
if got != 900:
    raise Exception('location test: got %s want 900' % got)

day2b = Location()
day2b.moves(day2_input)
print('Day 2 Part 2 :: %s' % day2b.mult())  # => 1599311480
