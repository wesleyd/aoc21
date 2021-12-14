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
    seed, rest = input.split('\n\n')
    rules = {}
    for line in rest.splitlines():
        l, r = line.split(' -> ')
        rules[l] = r
    return seed, rules


def apply(rules, before):
    after = [before[0]]
    for i in range(1, len(before)):
        k = before[i-1:i+1]
        if k in rules:
            after.append(rules[k])
        after.append(before[i])
    return ''.join(after)

def applyN(rules, polymer, N):
    for i in range(N):
        polymer = apply(rules, polymer)
    return polymer

seed, rules = parse(test_input)
got1 = apply(rules, seed)
want1 = 'NCNBCHB'
assert got1 == want1, 'test_input, #1: got %s, want %s' % (got1, want1)
got2 = apply(rules, got1)
want2 = 'NBCCNBBBCBHCB'
assert got2 == want2, 'test_input, #2: got %s, want %s' % (got2, want2)
got3 = apply(rules, got2)
want3 = 'NBBBCNCCNBBNBNBBCHBHHBCHB'
assert got3 == want3, 'test_input, #3: got %s, want %s' % (got3, want3)
got4 = apply(rules, got3)
want4 = 'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'
assert got4 == want4, 'test_input, #4: got %s, want %s' % (got4, want4)

def histo(polymer):
    h = defaultdict(int)
    for c in polymer:
        h[c] += 1
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

# Part 2
