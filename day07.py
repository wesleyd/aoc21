#!/usr/bin/env python3

import sys
from statistics import mean

day7_test_input = '16,1,2,0,4,2,7,1,2,14'

def parse(input):
    return list(map(int, input.split(',')))

def fuelto(pos, crabs):
    fuel = 0
    for c in crabs:
        fuel += abs(pos - c)
    return fuel

def minfuel(crabs, fuelto=fuelto):
    i = min(crabs)
    best = i
    bestfuel = sys.maxsize
    n = max(crabs)
    while i <= n:
        fuel = fuelto(i, crabs)
        if fuel < bestfuel:
            best = i
            bestfuel = fuel
        i += 1
    return best, bestfuel

crabs = parse(day7_test_input)
got, gotfuel = minfuel(crabs)
if got != 2 or gotfuel != 37:
    raise Exception('test got %d/%d want %d/37' % (got, gotfuel))

with open('inputs/day07.input') as f:
    crabs = parse(f.read())
    pos, fuel = minfuel(crabs)
    print('Day 7 Part 1 => position %d uses %d fuel => %d' % (pos, fuel, fuel))  # => 357353

### Part 2

def fuelto(pos, crabs):
    fuel = 0
    for c in crabs:
        delta = abs(pos - c)
        fuel += delta * (delta+1) // 2
    return fuel

with open('inputs/day07.input') as f:
    crabs = parse(f.read())
    pos, fuel = minfuel(crabs)
    print('Day 7 Part 2 => position %d uses %d fuel => %d' % (pos, fuel, fuel))  # => 104822130
