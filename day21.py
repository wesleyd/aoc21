#!/usr/bin/env python3

from collections import namedtuple
from collections import defaultdict

example_input = """\
Player 1 starting position: 4
Player 2 starting position: 8
"""

def parse(input):
    positions = []
    for line in input.splitlines():
        pieces = line.split(':')
        #print('pieces: %s' % pieces)
        positions.append(int(pieces[1]))
    return positions

class deterministic_die:
    def __init__(self, sides=100):
        self.sides = sides
        self.rolls = 0
        self.prev = 0
    def roll(self):
        self.rolls += 1
        self.prev += 1
        if self.prev > 100:
            self.prev = 1
        return self.prev

def play(positions):
    positions = [pos - 1 for pos in positions]  # Zero-index positions!
    scores = [0] * len(positions)
    d = deterministic_die()
    while True:
        for i in range(len(positions)):
            rr = [d.roll(),  d.roll(), d.roll()]
            positions[i] = (positions[i] + sum(rr)) % 10
            scores[i] += positions[i] + 1
            s = '+'.join([str(int(p)+1) for p in positions])
            if scores[i] >= 1000:
                j = (i + 1) % len(scores)  # i.e. the 'other' player id
                return scores[j] * d.rolls
assert play(parse(example_input)) == 739785

with open('inputs/day21.input') as f:
    positions = parse(f.read())
    print('Day 21 part 1 => %d' % play(positions))

# Part 2

# Each roll of three sided (!) dice produces this distribution of totals:
# 3x1 4x3 5x6 6x7 7x6 8x3 9x1
dice_histo = { 3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1 }
assert sum(dice_histo.values()) == 27

State = namedtuple('State', ['posA', 'scoreA', 'posB', 'scoreB'])

def parse_state(input):
    positions = parse(input)
    assert len(positions) == 2
    return State(positions[0], 0, positions[1], 0)
assert parse_state(example_input) == (4, 0, 8, 0)

def advance(pos, dice):
    assert 1 <= pos <= 10
    return (pos - 1 + dice) % 10 + 1
# Player 1 example
assert advance(4, 1+2+3) == 10
assert advance(10, 7+8+9) == 4
assert advance(4, 13+14+15) == 6
assert advance(6, 19+20+21) == 6
assert advance(4, 91+92+93) == 10
# Player 2 example
assert advance(8, 4+5+6) == 3
assert advance(3, 10+11+12) == 6
assert advance(6, 16+17+18) == 7
assert advance(7, 22+23+24) == 6
assert advance(6, 88+89+90) == 3

def dirac_play(states):
    if isinstance(states, State):
        states = defaultdict(int, {states: 1})
    winsA, winsB = 0, 0
    while states:
        states2 = defaultdict(int)
        for state, count in states.items():
            for dice, combosA in dice_histo.items():
                posA = advance(state.posA, dice)
                scoreA = state.scoreA + posA
                if scoreA >= 21:
                    winsA += count * combosA
                else:
                    for dice, combosB in dice_histo.items():
                        posB = advance(state.posB, dice)
                        scoreB = state.scoreB + posB
                        if scoreB >= 21:
                            winsB += count * (combosA * combosB)
                        else:
                            states2[State(posA, scoreA, posB, scoreB)] += count * (combosA * combosB)
        states = states2
    return winsA, winsB
assert dirac_play(parse_state(example_input)) == (444356092776315, 341960390180808)

with open('inputs/day21.input') as f:
    state = parse_state(f.read())
    winsA, winsB = dirac_play(state)
    wins = max(winsA, winsB)
    print('Day 21 part 2 => %d' % wins)
