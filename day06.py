#!/usr/bin/env python

import copy

day6_test_input = "3,4,3,1,2"

def parse(input):
    return list(map(int, input.split(",")))

def cycle(fishes):
    n = len(fishes)
    for i in range(n):
        if fishes[i] == 0:
            fishes.append(8)
            fishes[i] = 6
        else:
            fishes[i] -= 1
    return fishes

fishes = parse(day6_test_input)

def cycles(fishes, n):
    for i in range(n):
        fishes = cycle(fishes)
    return fishes

fishes_18 = cycles(parse(day6_test_input), 18)
if len(fishes_18) != 26:
    raise Exception('after 18 cycles, got %d want 26' % len(fishes_18))

fishes_80 = cycles(parse(day6_test_input), 80)
if len(fishes_80) != 5934:
    raise Exception('after 80 cycles, got %d want 26' % len(fishes_80))

with open("day06.input") as f:
    day6_input = list(map(int, f.read().split(',')))

fishes = copy.deepcopy(day6_input)
day6a = cycles(fishes, 80)
print("Day 6 Part 1 => %d fishes" % len(day6a))  # => 363101
