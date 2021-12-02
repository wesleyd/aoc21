#!/usr/bin/env python

import sys

def count_increases(depths):
    increases = 0
    for l, r in zip(depths[:-1], depths[1:]):
        if r > l:
            increases += 1
    return increases

def test_count_increases():
    got = count_increases([ 199, 200, 208, 210, 200, 207, 240, 269, 260, 263 ])
    want = 7
    if got != want:
        raise Exception('test_count_increases: got %d want %d' % (got, want))

test_count_increases()

def read_ints(filename):
    with open(filename) as f:
        return map(int, f)

count_increases(read_ints('day01.input'))  # => 1482
