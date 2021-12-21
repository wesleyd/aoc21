#!/usr/bin/env python3

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
            #print('Player %d rolls %s and moves to space %d for a total score of %d' % (i+1, s, positions[i]+1, scores[i]))
            if scores[i] >= 1000:
                j = (i + 1) % len(scores)  # i.e. the 'other' player id
                return scores[j] * d.rolls
assert play([4,8]) == 739785

def parse(input):
    positions = []
    for line in input.splitlines():
        pieces = line.split(':')
        print('pieces: %s' % pieces)
        positions.append(int(pieces[1]))
    return positions

with open('inputs/day21.input') as f:
    positions = parse(f.read())
    print('Day 21 part 1 => %d' % play(positions))

# Part 2
