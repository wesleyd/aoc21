#!/usr/bin/env python3

from collections import defaultdict

test_input = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

def parse(input):
    first, rest = input.split('\n\n')
    polymer = defaultdict(int)
    for i in range(1,len(first)):
        polymer[first[i-1:i+1]] += 1
    polymer[first[-1]] = 1  # Last element is special
    rules = {}
    for line in rest.splitlines():
        l, r = line.split(' -> ')
        rules[l] = r
    return polymer, rules

def apply(rules, before):
    polymer = defaultdict(int)
    for p, n in before.items():
        if len(p) == 1:  # Last element still special
            polymer[p] = n
            continue
        x = rules[p]
        q1 = p[0] + x
        q2 = x + p[1]
        polymer[q1] += n
        polymer[q2] += n
    return polymer

seed, rules = parse(test_input)
got1 = apply(rules, seed)
want1 = { 'BC': 1, 'CH': 1, 'CN': 1, 'HB': 1, 'NB': 1, 'NC': 1, 'B': 1 }
assert got1 == want1, 'test_input, #1: got %s, want %s' % (got1, want1)

def applyN(rules, polymer, N):
    for i in range(N):
        polymer = apply(rules, polymer)
    return polymer

def histo(polymer):
    h = defaultdict(int)
    for p, n in polymer.items():
        h[p[0]] += n
    return h

def spread(h):
    values = h.values()
    return max(values) - min(values)

polymer, rules = parse(test_input)
polymer = applyN(rules, polymer, 10)
got = histo(polymer)
want = {'B': 1749, 'C': 298, 'H': 161, 'N': 865}
assert got == want, 'histo after ten tries: got %s, want %s' % (got, want)
sp = spread(got)
assert sp == 1588

with open('day14.input') as f:
    seed, rules = parse(f.read())
    polymer = applyN(rules, seed, 10)
    h = histo(polymer)
    sp = spread(h)
    print('Day 14, part 1 => %d' % sp)  # => 3342

### Part 2

polymer, rules = parse(test_input)
polymer = applyN(rules, polymer, 40)
h = histo(polymer)
sp = spread(h)
assert sp == 2188189693529

with open('day14.input') as f:
    seed, rules = parse(f.read())
    polymer = applyN(rules, seed, 40)
    h = histo(polymer)
    sp = spread(h)
    print('Day 14, part 2 => %d' % sp)  # => 3776553567525
