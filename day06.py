#!/usr/bin/env python3

import copy
import collections

day6_test_input = "3,4,3,1,2"

def parse(input):
    school = collections.defaultdict(int)
    for f in map(int, input.split(",")):
        school[f] += 1
    return school

def nfishes(school):
    return sum(school.values())

def cycle(school):
    next = collections.defaultdict(int)
    for k, v in school.items():
        if k == 0:
            next[8] += v
            next[6] += v
        else:
            next[k-1] += v
    return next

def cycles(school, n):
    for i in range(n):
        school = cycle(school)
    return school

got = nfishes(cycles(parse(day6_test_input), 18))
if got != 26:
    raise Exception('after 18 cycles, got %d want 26' % got)

got = nfishes(cycles(parse(day6_test_input), 80))
if got != 5934:
    raise Exception('after 80 cycles, got %d want 26' % got)

with open("inputs/day06.input") as f:
    day6_input = f.read()

school = parse(day6_input)
day6a = nfishes(cycles(school, 80))
print("Day 6 Part 1 => %d fishes" % day6a)  # => 363101

### Part 2

got256 = nfishes(cycles(parse(day6_test_input), 256))
if got256 != 26984457539:
    raise Exception('after 256 cycles, got %d want 26984457539' % got256)

day6b = nfishes(cycles(parse(day6_input), 256))
print("Day 6 Part 2 => %d fishes" % day6b) # =>  1644286074024

