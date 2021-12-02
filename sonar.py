#!/usr/bin/env python

### Day 1

# Day 1 Part 1

def count_increases(depths):
    increases = 0
    for l, r in zip(depths[:-1], depths[1:]):
        if r > l:
            increases += 1
    return increases

day1_test_input = [ 199, 200, 208, 210, 200, 207, 240, 269, 260, 263 ]

def test_count_increases():
    got = count_increases(day1_test_input)
    want = 7
    if got != want:
        raise Exception('test_count_increases: got %d want %d' % (got, want))

test_count_increases()

def read_ints(filename):
    with open(filename) as f:
        return map(int, f)

day1_input = read_ints('day01.input')
day1a = count_increases(day1_input)  # => 1482
print "Day 1 Part 1: %d" % day1a

# Day 1 Part 2

def count_sliding_increases(depths):
    window = 3
    increases = 0
    prev = sum(depths[0:window])
    for i in range(window, len(depths)):
        next = prev + depths[i] - depths[i-window]
        if next > prev:
            increases += 1
        prev = next
    return increases

got = count_sliding_increases(day1_test_input)
want = 5
if got != want:
    raise Exception('test_count_increases: got %d want %d' % (got, want))

day1b = count_sliding_increases(day1_input)
print "Day 1 Part 2: %d" % day1b
